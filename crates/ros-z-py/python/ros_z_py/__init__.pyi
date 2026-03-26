"""Public re-exports for ros_z_py package (PEP 561)."""

from __future__ import annotations

from typing import Any, Callable, Final, Literal, TypeVar, overload

# Re-export message types from ros_z_msgs_py.types
from ros_z_msgs_py import types as types

# Re-export individual message packages for convenience
from ros_z_msgs_py.types import action_msgs as action_msgs
from ros_z_msgs_py.types import builtin_interfaces as builtin_interfaces
from ros_z_msgs_py.types import example_interfaces as example_interfaces
from ros_z_msgs_py.types import geometry_msgs as geometry_msgs
from ros_z_msgs_py.types import nav_msgs as nav_msgs
from ros_z_msgs_py.types import sensor_msgs as sensor_msgs
from ros_z_msgs_py.types import std_msgs as std_msgs
from ros_z_msgs_py.types import unique_identifier_msgs as unique_identifier_msgs

# service_msgs was introduced in ROS 2 Iron (May 2023) as part of the service
# introspection feature. It contains types like ServiceEventInfo for monitoring
# service calls. This package doesn't exist in Humble (May 2022).
try:
    from ros_z_msgs_py.types import service_msgs as service_msgs
except ImportError:
    pass

_MsgType = TypeVar("_MsgType")

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class RosZError(Exception): ...
class TimeoutError(RosZError): ...
class SerializationError(RosZError): ...
class TypeMismatchError(RosZError): ...

# ---------------------------------------------------------------------------
# QosProfile
# ---------------------------------------------------------------------------

class QosProfile:
    """Python QoS profile class with type-safe construction and presets.

    Example:
        qos = QosProfile(reliability="best_effort", history="keep_last", depth=5)
        pub = node.create_publisher("/topic", String, qos=qos)

        # Or use presets:
        pub = node.create_publisher("/topic", String, qos=QosProfile.sensor_data())
    """

    def __init__(
        self,
        reliability: str | None = None,
        durability: str | None = None,
        history: str | None = None,
        depth: int | None = None,
        liveliness: str | None = None,
        deadline: float | None = None,
        lifespan: float | None = None,
        liveliness_lease_duration: float | None = None,
    ) -> None:
        """Create a QoS profile with the given parameters.

        All parameters are optional and default to `QOS_DEFAULT` values.
        """
        ...

    @staticmethod
    def default() -> QosProfile:
        """Default QoS: Reliable, Volatile, KeepLast(10)."""
        ...

    @staticmethod
    def sensor_data() -> QosProfile:
        """Sensor data QoS: BestEffort, Volatile, KeepLast(5)."""
        ...

    @staticmethod
    def parameters() -> QosProfile:
        """Parameters QoS: Reliable, Volatile, KeepLast(1000)."""
        ...

    @staticmethod
    def services() -> QosProfile:
        """Services QoS: Reliable, Volatile, KeepLast(10)."""
        ...

    @property
    def reliability(self) -> str: ...
    @property
    def durability(self) -> str: ...
    @property
    def history(self) -> str: ...
    @property
    def depth(self) -> int: ...
    def __repr__(self) -> str: ...

# ---------------------------------------------------------------------------
# QoS constants
# ---------------------------------------------------------------------------

QOS_DEFAULT: Final[QosProfile] = QosProfile.default()
QOS_SENSOR_DATA: Final[QosProfile] = QosProfile.sensor_data()
QOS_PARAMETERS: Final[QosProfile] = QosProfile.parameters()
QOS_SERVICES: Final[QosProfile] = QosProfile.services()

# ---------------------------------------------------------------------------
# GoalStatus
# ---------------------------------------------------------------------------

class GoalStatus:
    """Goal status enum matching ROS 2 `action_msgs/msg/GoalStatus`."""

    UNKNOWN: int
    ACCEPTED: int
    EXECUTING: int
    CANCELING: int
    SUCCEEDED: int
    CANCELED: int
    ABORTED: int

    def __init__(self, value: int) -> None: ...
    @property
    def value(self) -> int: ...
    def is_active(self) -> bool: ...
    def is_terminal(self) -> bool: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...

# ---------------------------------------------------------------------------
# ZPayloadView — zero-copy buffer protocol wrapper
# ---------------------------------------------------------------------------

class ZPayloadView:
    """Zero-copy view of a Zenoh payload via Python buffer protocol.

    This class holds a Zenoh `Sample` and exposes its payload bytes through
    Python's buffer protocol. Python code can access the data without copying:

    ```python
    payload = subscriber.recv_raw_view()
    mv = memoryview(payload)  # Zero-copy view
    data = mv[offset:offset+length]  # Slicing is also zero-copy

    import numpy as np
    arr = np.frombuffer(payload, dtype=np.uint8)
    ```

    If the incoming payload is fragmented, the view falls back to an owned copy.
    """

    def __len__(self) -> int:
        """Return the payload length in bytes."""
        ...

    def __bool__(self) -> bool:
        """Return `True` if the payload is non-empty."""
        ...

    @property
    def is_zero_copy_py(self) -> bool:
        """Whether this view achieved zero-copy.

        Returns `True` if the payload was contiguous and no copy was needed.
        Returns `False` if the payload was fragmented and had to be copied.
        """
        ...

    def __buffer__(self, flags: int) -> memoryview:
        """Expose the payload through Python's buffer protocol.

        This is what powers `memoryview(payload)` and `numpy.frombuffer(payload)`.
        The exposed buffer is read-only.
        """
        ...

# ---------------------------------------------------------------------------
# ZContextBuilder
# ---------------------------------------------------------------------------

class ZContextBuilder:
    def __init__(self) -> None: ...
    def with_domain_id(self, domain_id: int) -> ZContextBuilder:
        """Set the ROS domain ID."""
        ...

    def with_logging_enabled(self) -> ZContextBuilder:
        """Enable Zenoh logging initialization with default level `"error"`."""
        ...

    def with_connect_endpoints(self, endpoints: list[str]) -> ZContextBuilder:
        """Connect to specific Zenoh endpoints such as `"tcp/127.0.0.1:7447"`."""
        ...

    def disable_multicast_scouting(self) -> ZContextBuilder:
        """Disable multicast scouting, useful for isolated tests."""
        ...

    def with_mode(self, mode: str) -> ZContextBuilder:
        """Set Zenoh mode: `"peer"`, `"client"`, or `"router"`."""
        ...

    def with_router_endpoint(self, endpoint: str) -> ZContextBuilder:
        """Connect to a router at the given endpoint."""
        ...

    def with_config_file(self, path: str) -> ZContextBuilder:
        """Load Zenoh configuration from a file."""
        ...

    def with_json(self, key: str, value: str) -> ZContextBuilder:
        """Add a JSON config override."""
        ...

    def with_remap_rule(self, rule: str) -> ZContextBuilder:
        """Add a name remap rule in `"from:=to"` format."""
        ...

    def with_remap_rules(self, rules: list[str]) -> ZContextBuilder:
        """Add multiple name remap rules."""
        ...

    def with_enclave(self, enclave: str) -> ZContextBuilder:
        """Set the security enclave name."""
        ...

    def connect_to_local_zenohd(self) -> ZContextBuilder:
        """Connect to a local `zenohd` router."""
        ...

    def with_shm_enabled(self) -> ZContextBuilder:
        """Enable Zenoh shared memory transport with the default pool size.

        SHM accelerates large message transfers between nodes on the same host.
        Both publisher and subscriber must have SHM enabled. Also enable SHM on
        the router if messages must be routed.

        Pool size and threshold can be overridden via
        `ZENOH_SHM_ALLOC_SIZE` and `ZENOH_SHM_MESSAGE_SIZE_THRESHOLD`,
        matching `rmw_zenoh_cpp` behavior.
        """
        ...

    def with_shm_pool_size(self, size_bytes: int) -> ZContextBuilder:
        """Enable SHM with a custom pool size in bytes.

        `ZENOH_SHM_MESSAGE_SIZE_THRESHOLD` still applies if set.
        """
        ...

    def with_shm_threshold(self, threshold: int) -> ZContextBuilder:
        """Set the minimum message size in bytes for SHM transport.

        Messages smaller than this threshold are sent via the network. Only
        effective after `with_shm_enabled()` or `with_shm_pool_size()`.
        """
        ...

    def build(self) -> ZContext:
        """Build the context."""
        ...

# ---------------------------------------------------------------------------
# ZContext
# ---------------------------------------------------------------------------

class ZContext:
    def __enter__(self) -> ZContext: ...
    def __exit__(self, *args: Any) -> None: ...
    def shutdown(self) -> None:
        """Shutdown the context and release all resources."""
        ...

    def create_node(self, name: str) -> ZNodeBuilder:
        """Create a node builder."""
        ...

# ---------------------------------------------------------------------------
# ZNodeBuilder
# ---------------------------------------------------------------------------

class ZNodeBuilder:
    """Builder for constructing a `ZNode`."""

    def with_namespace(self, namespace: str) -> ZNodeBuilder:
        """Set the namespace for the node."""
        ...

    def build(self) -> ZNode:
        """Build the node."""
        ...

# ---------------------------------------------------------------------------
# ZNode
# ---------------------------------------------------------------------------

class ZNode:
    """Python binding for a ros-z node."""

    @property
    def name(self) -> str:
        """Get the node name."""
        ...

    @property
    def namespace(self) -> str:
        """Get the node namespace."""
        ...

    @property
    def fully_qualified_name(self) -> str:
        """Get the fully qualified node name (`namespace + name`)."""
        ...

    def create_publisher(
        self,
        topic: str,
        msg_type: Any,
        qos: QosProfile | dict[str, object] | None = None,
    ) -> ZPublisher:
        """Create a publisher for a given topic and message type.

        Works with any registered message type without per-type factory limitations.
        """
        ...
    @overload
    def create_subscriber(
        self,
        topic: str,
        msg_type: type[_MsgType],
        qos: QosProfile | dict[str, object] | None = None,
        callback: Callable[[_MsgType], object] | None = None,
        raw: Literal[False] = False,
    ) -> ZSubscriber: ...
    @overload
    def create_subscriber(
        self,
        topic: str,
        msg_type: type[_MsgType],
        qos: QosProfile | dict[str, object] | None = None,
        callback: Callable[[ZPayloadView], object] | None = None,
        raw: Literal[True] = True,
    ) -> ZSubscriber: ...
    @overload
    def create_subscriber(
        self,
        topic: str,
        msg_type: type[_MsgType],
        qos: QosProfile | dict[str, object] | None = None,
        callback: (
            Callable[[_MsgType], object] | Callable[[ZPayloadView], object] | None
        ) = None,
        raw: bool = False,
    ) -> ZSubscriber: ...
    def create_subscriber(
        self,
        topic: str,
        msg_type: type[_MsgType],
        qos: QosProfile | dict[str, object] | None = None,
        callback: (
            Callable[[_MsgType], object] | Callable[[ZPayloadView], object] | None
        ) = None,
        raw: bool = ...,
    ) -> ZSubscriber:
        """Create a subscriber for a given topic and message type.

        Works with any registered message type without per-type factory limitations.

        If `callback` is provided:
        - `raw=False` (default) delivers a deserialized Python message object
        - `raw=True` delivers a `ZPayloadView`

        If `callback` is omitted, the returned subscriber uses the queue-based
        `recv()` / `try_recv()` APIs.
        """
        ...

    def create_client(self, service: str, srv_type: Any) -> ZClient:
        """Create a service client."""
        ...

    def create_server(self, service: str, srv_type: Any) -> ZServer:
        """Create a service server."""
        ...

    def create_action_client(
        self,
        action_name: str,
        goal_type: Any,
        result_type: Any,
        feedback_type: Any,
    ) -> ZActionClient:
        """Create an action client.

        `goal_type`, `result_type`, and `feedback_type` must be msgspec classes
        with `__msgtype__` and `__hash__` attributes from `ros_z_msgs_py`.

        Returns a `ZActionClient` for sending goals and receiving results.
        """
        ...

    def create_action_server(
        self,
        action_name: str,
        goal_type: Any,
        result_type: Any,
        feedback_type: Any,
    ) -> ZActionServer:
        """Create an action server.

        `goal_type`, `result_type`, and `feedback_type` must be msgspec classes
        with `__msgtype__` and `__hash__` attributes from `ros_z_msgs_py`.

        Returns a `ZActionServer` for receiving and executing goals.
        """
        ...

    def get_topic_names_and_types(self) -> list[tuple[str, str]]:
        """Get all topic names and their types.

        Returns a list of `(topic_name, type_name)` tuples.
        """
        ...

    def get_node_names(self) -> list[tuple[str, str]]:
        """Get all node names.

        Returns a list of `(name, namespace)` tuples.
        """
        ...

    def get_service_names_and_types(self) -> list[tuple[str, str]]:
        """Get all service names and their types.

        Returns a list of `(service_name, type_name)` tuples.
        """
        ...

    def count_publishers(self, topic: str) -> int:
        """Count publishers for a topic."""
        ...

    def count_subscribers(self, topic: str) -> int:
        """Count subscribers for a topic."""
        ...

    def destroy_subscriber(self, sub: ZSubscriber) -> None:
        """Destroy a callback-based subscriber early.

        Matches `rclpy.Node.destroy_subscription()`. Has no effect on queue-based
        subscribers, which are owned by the caller and dropped when they go out
        of scope.
        """
        ...

# ---------------------------------------------------------------------------
# ZPublisher
# ---------------------------------------------------------------------------

class ZPublisher:
    """Publisher wrapper for sending topic data."""

    def publish(self, data: Any) -> None:
        """Publish a message.

        Serializes the Python message and publishes it using the zero-copy ZBuf path.
        """
        ...

    def publish_raw(
        self, data: ZPayloadView | bytes | bytearray | memoryview
    ) -> None:
        """Publish pre-serialized CDR data directly.

        Accepts a `ZPayloadView` for zero-copy forwarding of the underlying Zenoh
        payload handle, or any contiguous Python buffer object such as `bytes`,
        `bytearray`, or `memoryview`.
        """
        ...

    def get_type_name(self) -> str:
        """Get the topic type name, mainly for debugging."""
        ...

# ---------------------------------------------------------------------------
# ZSubscriber
# ---------------------------------------------------------------------------

class ZSubscriber:
    """Subscriber wrapper for receiving topic data."""

    @property
    def is_callback(self) -> bool:
        """Whether this is a callback-based subscriber with no recv methods."""
        ...

    def recv(self, timeout: float | None = None) -> Any | None:
        """Receive the next message.

        Args:
            timeout: Optional timeout in seconds. `None` blocks forever.

        Returns:
            The deserialized message object, or `None` if the timeout expires.
        """
        ...

    def try_recv(self) -> Any | None:
        """Try to receive a message without blocking.

        Returns:
            The deserialized message object, or `None` if no message is available.
        """
        ...

    def recv_serialized(self, timeout: float | None = None) -> bytes | None:
        """Receive serialized CDR bytes.

        Intended for testing and advanced use.
        """
        ...

    def try_recv_serialized(self) -> bytes | None:
        """Try to receive serialized CDR bytes without blocking."""
        ...

    def recv_raw_view(self, timeout: float | None = None) -> ZPayloadView | None:
        """Receive the next payload as a `ZPayloadView`.

        The returned object implements Python's buffer protocol, so it can be used
        with `memoryview()` or `numpy.frombuffer()` for zero-copy access.
        """
        ...

    def try_recv_raw_view(self) -> ZPayloadView | None:
        """Try to receive the next payload as a `ZPayloadView` without blocking."""
        ...

    def get_type_name(self) -> str:
        """Get the topic type name, mainly for debugging."""
        ...

# ---------------------------------------------------------------------------
# ZClient (service client)
# ---------------------------------------------------------------------------

class ZClient:
    """Service client wrapper."""

    def send_request(self, data: Any) -> None:
        """Send a service request."""
        ...

    def take_response(self, timeout: float | None = None) -> Any | None:
        """Receive a service response.

        Args:
            timeout: Optional timeout in seconds. `None` blocks forever.
        """
        ...

    def try_take_response(self) -> Any | None:
        """Try to receive a service response without blocking."""
        ...

    def get_type_name(self) -> str:
        """Get the service request/response type names, mainly for debugging."""
        ...

# ---------------------------------------------------------------------------
# ZServer (service server)
# ---------------------------------------------------------------------------

class ZServer:
    """Service server wrapper."""

    def take_request(self) -> tuple[dict[str, Any], Any]:
        """Receive the next service request.

        Returns a `(request_id, request)` pair. The `request_id` must be passed
        back to `send_response()`.
        """
        ...

    def send_response(self, response: Any, request_id: dict[str, Any]) -> None:
        """Send a response to a service request."""
        ...

    def get_type_name(self) -> str:
        """Get the service request/response type names, mainly for debugging."""
        ...

# ---------------------------------------------------------------------------
# ZActionClient
# ---------------------------------------------------------------------------

class ZActionClient:
    """Python wrapper for an action client.

    Created via
    `node.create_action_client(action_name, goal_type, result_type, feedback_type)`.
    """

    def send_goal(self, goal: Any) -> ActionGoalHandle:
        """Send a goal and block until the server accepts or rejects it.

        Returns an `ActionGoalHandle` on success and raises on rejection or error.
        """
        ...

    @property
    def goal_type(self) -> Any:
        """Get the goal type class, mainly for debugging."""
        ...

# ---------------------------------------------------------------------------
# ActionGoalHandle (client side)
# ---------------------------------------------------------------------------

class ActionGoalHandle:
    """Handle for a goal sent to an action server.

    Returned by `ZActionClient.send_goal()`. Allows receiving feedback,
    checking status, canceling, and retrieving the final result.
    """

    @property
    def goal_id(self) -> bytes:
        """Return the goal ID as bytes (16-byte UUID)."""
        ...

    @property
    def status(self) -> int:
        """Current goal status as an integer matching `GoalStatus` constants."""
        ...

    def recv_feedback(self, timeout: float | None = None) -> Any | None:
        """Receive the next feedback message.

        Returns `None` on timeout or if the feedback channel is closed.
        """
        ...

    def try_recv_feedback(self) -> Any | None:
        """Try to receive feedback without blocking."""
        ...

    def get_result(self, timeout: float | None = None) -> Any | None:
        """Wait for and return the final result.

        Consumes the goal handle internally. Returns `None` on timeout and raises
        `RuntimeError` if called more than once.
        """
        ...

    def cancel(self) -> None:
        """Request cancellation of this goal."""
        ...

# ---------------------------------------------------------------------------
# ZActionServer
# ---------------------------------------------------------------------------

class ZActionServer:
    """Python wrapper for an action server.

    Created via
    `node.create_action_server(action_name, goal_type, result_type, feedback_type)`.

    Server loop pattern:

    ```python
    server = node.create_action_server("/navigate", Goal, Result, Feedback)
    while True:
        request = server.recv_goal(timeout=1.0)
        if request is None:
            continue
        executing = request.accept_and_execute()
        executing.publish_feedback(Feedback(progress=0.5))
        executing.succeed(Result(success=True))
    ```
    """

    def recv_goal(self, timeout: float | None = None) -> ServerGoalRequest | None:
        """Wait for the next goal request.

        Returns a `ServerGoalRequest` on success, or `None` on timeout.
        """
        ...

# ---------------------------------------------------------------------------
# ServerGoalRequest (requested state — not yet accepted/rejected)
# ---------------------------------------------------------------------------

class ServerGoalRequest:
    """A goal request received by the action server.

    This request has not yet been accepted or rejected.
    """

    @property
    def goal_id(self) -> bytes:
        """The goal ID as bytes (16-byte UUID)."""
        ...

    def goal(self) -> Any:
        """The goal as a Python object."""
        ...

    def accept_and_execute(self) -> ServerGoalHandle:
        """Accept this goal request and begin execution.

        Returns a `ServerGoalHandle` for the executing goal.
        Raises `RuntimeError` if the request was already accepted or rejected.
        """
        ...

    def reject(self) -> None:
        """Reject this goal request. The client will receive an error."""
        ...

# ---------------------------------------------------------------------------
# ServerGoalHandle (executing state)
# ---------------------------------------------------------------------------

class ServerGoalHandle:
    """Handle for an accepted and executing action goal.

    Returned by `ServerGoalRequest.accept_and_execute()`.
    """

    @property
    def goal_id(self) -> bytes:
        """The goal ID as bytes (16-byte UUID)."""
        ...

    def goal(self) -> Any:
        """The goal as a Python object."""
        ...

    @property
    def is_cancel_requested(self) -> bool:
        """Whether the client has requested cancellation of this goal.

        This also processes any pending cancel service request from the cancel
        queue in non-blocking polling mode.
        """
        ...

    def publish_feedback(self, feedback: Any) -> None:
        """Publish a feedback message to the client."""
        ...

    def succeed(self, result: Any) -> None:
        """Mark the goal as succeeded with the given result."""
        ...

    def abort(self, result: Any) -> None:
        """Mark the goal as aborted with the given result."""
        ...

    def canceled(self, result: Any) -> None:
        """Mark the goal as canceled with the given result."""
        ...

# ---------------------------------------------------------------------------
# Free functions
# ---------------------------------------------------------------------------

def list_registered_types() -> list[str]:
    """Get the list of all registered message types."""
    ...
