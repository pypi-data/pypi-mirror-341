import asyncio
import json
import time
import threading
from typing import Dict, Any, Optional, Callable, Tuple
import logging
import argparse
import os
import getpass
import socket
import websockets
from websockets.exceptions import ConnectionClosed


class GARClient:
    """
    A client implementation for the Generic Active Records (GAR) protocol using WebSockets.

    The GARClient class provides a Python interface for connecting to a GAR server
    using WebSockets as the transport layer. It handles the protocol details including
    message serialization, heartbeat management, topic and key enumeration, record
    updates, and subscription management.

    The client maintains separate mappings for server-assigned and client-assigned
    topic and key IDs, allowing for independent enumeration on both sides. It provides
    methods for subscribing to data, publishing records, and registering handlers for
    various message types.

    Key features:
    - Automatic heartbeat management to maintain connection
    - Support for topic and key int <-> string introductions
    - Record creation, updating, and deletion
    - Subscription management with filtering options
    - Customizable message handlers for all protocol message types
    - Thread-safe message sending
    - Automatic reconnection on WebSocket connection loss

    Example usage:
        client = GARClient("ws://localhost:8765", "username")

        # Register custom handlers
        client.register_record_update_handler(lambda key_id, topic_id, value:
            print(f"Update: {key_id}-{topic_id} = {value}"))

        # Start the client in a separate thread
        client_thread = threading.Thread(target=client.start)
        client_thread.start()

        # Subscribe to data
        client.subscribe("MySubscription", mode="Streaming")

        # Publish a record
        client.publish_record("AAPL", "price", 150.25)

        # Clean shutdown
        client.logoff()
        client_thread.join()

    See the full documentation at https://trinityriversystems.com/docs/ for detailed
    protocol specifications and usage instructions.
    """

    def __init__(self, ws_endpoint: str, user: str, heartbeat_interval: int = 4000):
        """
        Initialize the GAR (Generic Active Records) client.

        Creates a new GAR client instance that connects to a GAR server using WebSockets.
        The client establishes a connection with a unique identity based on hostname,
        username, and process ID. It sets up internal data structures for tracking
        topics, keys, and message handlers, and initializes the heartbeat mechanism
        for maintaining the connection.

        Args:
            ws_endpoint: WebSocket endpoint string in the format "ws://address:port"
                         (e.g., "ws://localhost:8765") where the GAR server is listening.
            user: Client username string used for identification and authentication
                  with the server. This is included in the socket identity.
            heartbeat_interval: Time in milliseconds between heartbeat messages sent
                               to the server to maintain the connection. Default is 4000ms (4 seconds).

        Returns:
            None

        Note:
            The client is not started automatically after initialization.
            Call the start() method to begin communication with the server.
        """
        self.ws_endpoint = ws_endpoint
        # pylint: disable=no-member
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.connected = False
        self.reconnect_delay = 5.0  # Seconds to wait before reconnecting

        hostname = socket.gethostname()
        pid = os.getpid()
        self.identity = f"{hostname}:{user}:{pid}"
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Set client identity: %s", self.identity)

        self.user = user
        self.heartbeat_interval = heartbeat_interval
        self.version = 650269

        self.server_topic_map: Dict[int, str] = {}
        self.server_key_map: Dict[int, str] = {}

        self.local_topic_counter = 1
        self.local_key_counter = 1
        self.local_topic_map: Dict[str, int] = {}
        self.local_key_map: Dict[str, int] = {}

        self.running = False
        self.heartbeat_thread = None

        self.message_handlers: Dict[str, Callable[[Dict[str, Any]], None]] = {}

        self.last_heartbeat_time = time.time()
        self.heartbeat_timeout = 3  # Default 3 seconds
        # for “10× grace” on the very first heartbeat
        self._initial_grace_period = False
        self._initial_grace_deadline = 0.0

        self.heartbeat_timeout_callback: Optional[Callable[[], None]] = None
        self.stopped_callback: Optional[Callable[[], None]] = None

        self.send_lock = threading.Lock()
        self.record_map: Dict[Tuple[int, int], Any] = {}

        logging.basicConfig(level=logging.INFO)
        self.register_default_handlers()

        # Asyncio event loop for WebSocket operations
        self.loop = asyncio.new_event_loop()

    async def connect(self):
        """Establish WebSocket connection with reconnection logic, using GAR subprotocol."""
        while self.running and not self.connected:
            try:
                # Include the GAR protocol in the handshake
                async with websockets.connect(
                        self.ws_endpoint,
                        subprotocols=["gar-protocol"]
                ) as websocket:
                    self.websocket = websocket
                    self.connected = True
                    self.logger.info("Connected to WebSocket server at %s using gar-protocol", self.ws_endpoint)
                    await asyncio.gather(self._send_messages(), self._receive_messages())
            except (ConnectionClosed, ConnectionRefusedError) as e:
                self.logger.error(
                    "WebSocket connection failed: %s. Reconnecting in %s seconds...", e, self.reconnect_delay
                )
                self.connected = False
                self.websocket = None
                await asyncio.sleep(self.reconnect_delay)


    async def _send_messages(self):
        """Send messages from the queue to the WebSocket server."""
        while self.connected:
            try:
                message = await self.message_queue.get()
                if self.websocket:
                    await self.websocket.send(json.dumps(message))
                    self.logger.debug("Sent: %s", json.dumps(message))
                self.message_queue.task_done()
            except ConnectionClosed:
                self.logger.warning("Connection closed while sending. Queuing message for retry.")
                self.stop()
                await self.message_queue.put(message)
                break
            except Exception as e:
                self.logger.error("Error sending message: %s", e)
                break

    async def _receive_messages(self):
        """Receive and process messages from the WebSocket server."""
        while self.connected:
            try:
                if self.websocket:
                    message = await self.websocket.recv()
                    msg = json.loads(message)
                    # pylint: disable=no-member
                    self._process_message(msg)
            except ConnectionClosed:
                self.logger.warning("Connection closed while receiving.")
                self.stop()
                break
            except json.JSONDecodeError as e:
                self.logger.error("Invalid JSON received: %s", e)
            except Exception as e:
                self.logger.error("Error receiving message: %s", e)
                break

    def register_handler(self, message_type: str, handler: Callable[[Dict[str, Any]], None]):
        """Register a callback handler for a specific message type."""
        self.message_handlers[message_type] = handler

    def register_introduction_handler(self, handler: Callable[[int, int, str, Optional[str]], None]):
        """Handler for Introduction: (version, heartbeat_timeout_interval, user, schema)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["version"], value["heartbeat_timeout_interval"],
                    value["user"], value.get("schema"))

        self.register_handler("Introduction", wrapper)

    def register_heartbeat_handler(self, handler: Callable[[], None]):
        """Handler for Heartbeat: no arguments"""

        # pylint: disable=W0613
        def wrapper(msg: Dict[str, Any]):
            handler()

        self.register_handler("Heartbeat", wrapper)

    def clear_heartbeat_handler(self):
        """Remove the registered heartbeat handler."""
        self.message_handlers.pop("Heartbeat", None)

    def register_logoff_handler(self, handler: Callable[[], None]):
        """Handler for Logoff: no arguments"""

        # pylint: disable=W0613
        def wrapper(msg: Dict[str, Any]):
            handler()

        self.register_handler("Logoff", wrapper)

    def register_topic_introduction_handler(self, handler: Callable[[int, str], None]):
        """Handler for TopicIntroduction: (topic_id, name)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["topic_id"], value["name"])

        self.register_handler("TopicIntroduction", wrapper)

    def register_key_introduction_handler(self, handler: Callable[[int, str, Optional[str]], None]):
        """Handler for KeyIntroduction: (key_id, name, _class)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["key_id"], value["name"], value.get("_class"))

        self.register_handler("KeyIntroduction", wrapper)

    def register_delete_key_handler(self, handler: Callable[[int], None]):
        """Handler for DeleteKey: (key_id)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["key_id"])

        self.register_handler("DeleteKey", wrapper)

    def register_subscribe_handler(self, handler: Callable[[str, int, str, int, int, Optional[str], Optional[str], Optional[str]], None]):
        """Handler for Subscribe: (subscription_mode, nagle_interval, name, key_id, topic_id, _class, key_filter, topic_filter)"""

        def wrapper(msg: Dict[str, Any]):
            value = msg["value"]
            handler(value["subscription_mode"], value["nagle_interval"], value["name"],
                    value["key_id"], value["topic_id"], value.get("_class"),
                    value.get("key_filter"), value.get("topic_filter"))

        self.register_handler("Subscribe", wrapper)

    def register_snapshot_complete_handler(self, handler: Callable[[str], None]):
        """Handler for SnapshotComplete: (name)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["name"])

        self.register_handler("SnapshotComplete", wrapper)

    def register_unsubscribe_handler(self, handler: Callable[[str], None]):
        """Handler for Unsubscribe: (name)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["name"])

        self.register_handler("Unsubscribe", wrapper)

    def register_delete_record_handler(self, handler: Callable[[int, int], None]):
        """Handler for DeleteRecord: (key_id, topic_id)"""

        def wrapper(msg: Dict[str, Any]):
            handler(msg["value"]["key_id"], msg["value"]["topic_id"])

        self.register_handler("DeleteRecord", wrapper)

    def register_record_update_handler(self, handler: Callable[[int, int, Any], None]):
        """Handler for JSONRecordUpdate: (key_id, topic_id, value)"""

        def wrapper(msg: Dict[str, Any]):
            record_id = msg["value"]["record_id"]
            handler(record_id["key_id"], record_id["topic_id"], msg["value"]["value"])

        self.register_handler("JSONRecordUpdate", wrapper)

    def register_shutdown_handler(self, handler: Callable[[], None]):
        """Handler for Shutdown: no arguments"""

        # pylint: disable=W0613
        def wrapper(msg: Dict[str, Any]):
            handler()

        self.register_handler("Shutdown", wrapper)

    def register_heartbeat_timeout_handler(self, handler: Callable[[], None]):
        """Register a callback to handle heartbeat timeout events."""
        self.heartbeat_timeout_callback = handler

    def register_stopped_handler(self, handler: Callable[[], None]):
        """Register a callback to handle client stopped events."""
        self.stopped_callback = handler

    def register_default_handlers(self):
        """Register default logging handlers for all message types."""
        self.register_introduction_handler(
            lambda version, interval, user, schema: self.logger.info("Connected to server: %s", user))
        self.register_heartbeat_handler(
            lambda: self.logger.debug("Heartbeat received"))
        self.register_logoff_handler(
            lambda: self.logger.info("Logoff received"))
        self.register_topic_introduction_handler(
            lambda topic_id, name: self.logger.info("New server topic: %s (Server ID: %d)", name, topic_id))
        self.register_key_introduction_handler(
            lambda key_id, name, _class: self.logger.info("New server key: %s (Server ID: %d)", name, key_id))
        self.register_delete_key_handler(
            lambda key_id: self.logger.info("Delete key: %s (Server ID: %d)", self.server_key_map.get(key_id), key_id))
        self.register_subscribe_handler(
            lambda mode, interval, name, key_id, topic_id, _class, key_filter, topic_filter:
            self.logger.info("Subscribe: %s (mode: %s)", name, mode))
        self.register_snapshot_complete_handler(
            lambda name: self.logger.info("Snapshot complete for subscription: %s", name))
        self.register_unsubscribe_handler(
            lambda name: self.logger.info("Unsubscribe: %s", name))
        self.register_delete_record_handler(
            lambda key_id, topic_id: self.logger.info(
                "Delete record: %s - %s", self.server_key_map.get(key_id), self.server_topic_map.get(topic_id)))
        self.register_record_update_handler(
            lambda key_id, topic_id, value: self.logger.info(
                "Record update: %s - %s = %s", self.server_key_map.get(key_id), self.server_topic_map.get(topic_id), value))
        self.register_shutdown_handler(
            lambda: self.logger.info("Shutdown received"))

    def start(self):
        """Start the client and send introduction message."""
        self.running = True
        intro_msg = {
            "message_type": "Introduction",
            "value": {
                "version": self.version,
                "heartbeat_timeout_interval": self.heartbeat_interval,
                "user": self.user
            }
        }
        self.send_message(intro_msg)
        # pylint: disable=no-member
        self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self.heartbeat_thread.start()
        # Run the WebSocket connection in the asyncio event loop
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.connect())
        self.loop.close()

    def logoff(self):
        """Send a logoff message to the server and stop the client."""
        self.send_message({"message_type": "Logoff"})
        self.stop()

    def stop(self):
        """Stop the client and terminate all client operations."""
        self.running = False
        self.connected = False
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)
        if self.stopped_callback:
            try:
                self.stopped_callback()
            except Exception as e:
                self.logger.error("Error in stopped callback: %s", e)

    def __del__(self):
        """Clean up resources when the object is destroyed."""
        if self.loop and not self.loop.is_closed():
            self.loop.close()

    def send_message(self, message: Dict[str, Any]):
        """Send a JSON message through the WebSocket."""
        with self.send_lock:
            asyncio.run_coroutine_threadsafe(self.message_queue.put(message), self.loop)

    def _heartbeat_loop(self):
        """Send periodic heartbeat messages."""
        while self.running:
            self.send_message({"message_type": "Heartbeat"})
            time.sleep(self.heartbeat_interval / 1000 / 2)

    # pylint: disable=too-many-statements
    def _process_message(self, message: Dict[str, Any]):
        """Process incoming messages by calling registered handlers."""
        msg_type = message.get("message_type")
        if msg_type == "TopicIntroduction":
            self.server_topic_map[message["value"]["topic_id"]] = message["value"]["name"]
        elif msg_type == "KeyIntroduction":
            self.server_key_map[message["value"]["key_id"]] = message["value"]["name"]
        elif msg_type == "DeleteKey":
            # 1) drop deleted key from server map
            key_id = message["value"]["key_id"]
            self.server_key_map.pop(key_id, None)
        elif msg_type == "Heartbeat":
            # update last‐beat and clear initial grace on the very first one
            self.last_heartbeat_time = time.time()
            if self._initial_grace_period:
                self._initial_grace_period = False
        elif msg_type == "Introduction":
            value = message["value"]
            # 5) Clear out old server state on reconnect
            self.server_topic_map.clear()
            self.server_key_map.clear()
            self.record_map.clear()
            # reset heartbeat timeout (in seconds)
            self.heartbeat_timeout = max(self.heartbeat_timeout,
                                         value["heartbeat_timeout_interval"] / 1000)
            self.last_heartbeat_time = time.time()
            # 4) enable 10× grace window for the *first* heartbeat
            self._initial_grace_period = True
            self._initial_grace_deadline = (self.last_heartbeat_time +
                                            self.heartbeat_timeout * 10)
        elif msg_type == "JSONRecordUpdate":
            record_id = message["value"]["record_id"]
            key_id = record_id["key_id"]
            topic_id = record_id["topic_id"]
            record_value = message["value"]["value"]
            self.record_map[(key_id, topic_id)] = record_value
        elif msg_type == "DeleteRecord":
            value = message["value"]
            key_id = value["key_id"]
            topic_id = value["topic_id"]
            self.record_map.pop((key_id, topic_id), None)
        elif msg_type == "Logoff":
            self.logger.info("Received Logoff from server, shutting down")
            self.running = False
            return

        # Enforce heartbeat timeout, with 10× grace for the very first beat
        now = time.time()
        if self._initial_grace_period:
            if now > self._initial_grace_deadline:
                self.logger.warning("No initial heartbeat within %d seconds",
                                    int(self.heartbeat_timeout * 10))
                self.running = False
                if self.heartbeat_timeout_callback:
                    self.heartbeat_timeout_callback()
                return
        else:
            if now - self.last_heartbeat_time > self.heartbeat_timeout:
                self.logger.warning("No heartbeat received within %d seconds",
                                    int(self.heartbeat_timeout))
                self.running = False
                if self.heartbeat_timeout_callback:
                    self.heartbeat_timeout_callback()
                return

        handler = self.message_handlers.get(msg_type)
        if handler:
            handler(message)
        else:
            self.logger.debug("No handler registered for message type: %s", msg_type)

    # pylint: disable=unused-variable
    def subscribe(self, name: str, mode: str = "Streaming",
                  key_name: Optional[str] = None, topic_name: Optional[str] = None,
                  class_filter: Optional[str] = None, key_filter: Optional[str] = None,
                  topic_filter: Optional[str] = None):
        """Send a subscription request using local IDs."""
        key_id = self.get_and_possibly_introduce_key_id(key_name) if key_name else 0
        topic_id = self.get_and_possibly_introduce_topic_id(topic_name) if topic_name else 0
        sub_msg = {
            "message_type": "Subscribe",
            "value": {
                "subscription_mode": mode,
                "nagle_interval": 0,
                "name": name,
                "key_id": key_id,
                "topic_id": topic_id,
                "_class": class_filter,
                "key_filter": key_filter,
                "topic_filter": topic_filter
            }
        }
        self.send_message(sub_msg)

    # pylint: disable=unused-variable
    def get_and_possibly_introduce_key_id(self, name: str, class_name: Optional[str] = None) -> int:
        """Introduce a new key if not already known and return local key ID."""
        if name not in self.local_key_map:
            key_id = self.local_key_counter
            self.local_key_map[name] = key_id
            self.local_key_counter += 1
            msg = {
                "message_type": "KeyIntroduction",
                "value": {
                    "key_id": key_id,
                    "name": name,
                    "_class": class_name
                }
            }
            self.send_message(msg)
        return self.local_key_map[name]

    # pylint: disable=unused-variable
    def get_and_possibly_introduce_topic_id(self, name: str) -> int:
        """Introduce a new topic if not already known and return local topic ID."""
        if name not in self.local_topic_map:
            topic_id = self.local_topic_counter
            self.local_topic_map[name] = topic_id
            self.local_topic_counter += 1
            msg = {
                "message_type": "TopicIntroduction",
                "value": {
                    "topic_id": topic_id,
                    "name": name
                }
            }
            self.send_message(msg)
        return self.local_topic_map[name]

    # pylint: disable=unused-variable
    def publish_delete_key(self, key_id: int):
        """Publish a DeleteKey message using a local key ID."""
        msg = {
            "message_type": "DeleteKey",
            "value": {
                "key_id": key_id
            }
        }
        self.send_message(msg)

    # pylint: disable=unused-variable
    def publish_delete_record(self, key_id: int, topic_id: int):
        """Publish a DeleteRecord message using local key and topic IDs."""
        msg = {
            "message_type": "DeleteRecord",
            "value": {
                "key_id": key_id,
                "topic_id": topic_id
            }
        }
        self.send_message(msg)

    # pylint: disable=unused-variable
    def publish_unsubscribe(self, name: str):
        """Publish an Unsubscribe message for a subscription name."""
        msg = {
            "message_type": "Unsubscribe",
            "value": {
                "name": name
            }
        }
        self.send_message(msg)

    # pylint: disable=unused-variable
    def publish_shutdown(self):
        """Publish a Shutdown message."""
        msg = {
            "message_type": "Shutdown"
        }
        self.send_message(msg)

    # pylint: disable=unused-variable
    def publish_record_with_ids(self, key_id: int, topic_id: int, value: Any):
        """
        Publish a record update using explicit key and topic IDs.

        This method creates and sends a JSONRecordUpdate message to the GAR server
        using the provided key and topic IDs. Unlike publish_record(), this method
        does not perform any name-to-ID conversion or introduce new keys/topics.

        Args:
            key_id: The integer ID of the key for this record. This should be a valid
                   key ID that has already been introduced to the server.
            topic_id: The integer ID of the topic for this record. This should be a valid
                     topic ID that has already been introduced to the server.
            value: The value to publish for this record. Can be any JSON-serializable
                  data type (dict, list, string, number, boolean, or null).

        Returns:
            None
        """
        update_msg = {
            "message_type": "JSONRecordUpdate",
            "value": {
                "record_id": {
                    "key_id": key_id,
                    "topic_id": topic_id
                },
                "value": value
            }
        }
        self.send_message(update_msg)

    # pylint: disable=unused-variable
    def publish_record(self, key_name: str, topic_name: str, value: Any):
        """Publish a record update using names, converting to local IDs."""
        key_id = self.get_and_possibly_introduce_key_id(key_name)
        topic_id = self.get_and_possibly_introduce_topic_id(topic_name)
        self.publish_record_with_ids(key_id, topic_id, value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GAR Protocol Client")
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="WebSocket IP address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765,
                        help="WebSocket port (default: 8765)")
    parser.add_argument("--user", type=str, default=None,
                        help="Username (default: OS environment username)")
    parser.add_argument("--log-level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="Logging level (default: INFO)")
    parser.add_argument("--streaming", action="store_true",
                        help="Stay running and stream updates. Otherwise exit after snapshot received.")
    parser.add_argument("--key-filter", type=str, default=None,
                        help="Key filter regex pattern")
    parser.add_argument("--class", type=str, default=None,
                        help="Class name")
    parser.add_argument("--topic-filter", type=str, default=None,
                        help="Topic filter regex pattern")
    parser.add_argument("--send-shutdown", action="store_true",
                        help="Shut down the server")

    args = parser.parse_args()
    username = args.user if args.user is not None else getpass.getuser()
    endpoint = f"ws://{args.ip}:{args.port}"

    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=log_level)

    client = GARClient(endpoint, username)


    # pylint: disable=C0116,W0613

    def custom_topic_handler(c, topic_id: int, name: str):
        logging.info("Custom topic: %s (ID: %d)", name, topic_id)


    def custom_record_update_handler(c, key_id: int, topic_id: int, value: Any):
        key_name = client.server_key_map.get(key_id, "Unknown")
        topic_name = client.server_topic_map.get(topic_id, "Unknown")
        logging.info("Custom update: %s %s = %s", key_name, topic_name, value)


    def custom_delete_key_handler(c, key_id: int):
        key_name = client.server_key_map.get(key_id, "Unknown")
        logging.info("Custom delete key: %s (ID: %d)", key_name, key_id)


    client.register_topic_introduction_handler(lambda topic_id, name: custom_topic_handler(client, topic_id, name))
    client.register_record_update_handler(lambda key_id, topic_id, value: custom_record_update_handler(client, key_id, topic_id, value))
    client.register_delete_key_handler(lambda key_id: custom_delete_key_handler(client, key_id))

    try:
        client_thread = threading.Thread(target=client.start)
        client_thread.start()

        # Need to release the GIL for the client thread to send introduction
        time.sleep(1)

        if args.send_shutdown:
            client.publish_shutdown()
            client.logoff()
        else:
            SUBSCRIPTION_MODE = "Streaming" if args.streaming else "Snapshot"
            client.subscribe("S1", mode=SUBSCRIPTION_MODE,
                             key_name=None, topic_name=None,
                             class_filter=args.__dict__["class"],
                             key_filter=args.key_filter,
                             topic_filter=args.topic_filter)

            if SUBSCRIPTION_MODE == "Snapshot":
                client.logoff()

        client_thread.join()

    except KeyboardInterrupt:
        client.stop()
