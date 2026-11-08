"""
AERO-Swarm: Dual-Mode ROS 2 Compatibility Bridge
Provides transparent fallback pub/sub bus, message structures, and Node base class
when running on platforms without native ROS 2 Humble (e.g. Windows).
When native rclpy is installed (e.g. Ubuntu 22.04), seamlessly delegates to official ROS 2.
"""

import sys
import time
import threading
from typing import Callable, Any, Dict, List

# Check if native rclpy exists
try:
    import rclpy as _native_rclpy
    from rclpy.node import Node as _NativeNode
    HAS_NATIVE_ROS2 = True
except ImportError:
    HAS_NATIVE_ROS2 = False


# ==============================================================================
# Transparent ROS Message Mimics (Pure Python)
# ==============================================================================

class _Vector3:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

class _Point:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

class _Quaternion:
    def __init__(self, x=0.0, y=0.0, z=0.0, w=1.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

class _Pose:
    def __init__(self):
        self.position = _Point()
        self.orientation = _Quaternion()

class _PoseWithCovariance:
    def __init__(self):
        self.pose = _Pose()
        self.covariance = [0.0] * 36

class _Twist:
    def __init__(self):
        self.linear = _Vector3()
        self.angular = _Vector3()

class _TwistWithCovariance:
    def __init__(self):
        self.twist = _Twist()
        self.covariance = [0.0] * 36

class _Header:
    def __init__(self):
        self.stamp = _TimeMsg()
        self.frame_id = ""

class Odometry:
    def __init__(self):
        self.header = _Header()
        self.pose = _PoseWithCovariance()
        self.twist = _TwistWithCovariance()

class Twist:
    def __init__(self):
        self.linear = _Vector3()
        self.angular = _Vector3()

class Float64MultiArray:
    def __init__(self, data: List[float] = None):
        self.data = list(data) if data is not None else []

class Int32MultiArray:
    def __init__(self, data: List[int] = None):
        self.data = list(data) if data is not None else []

class Float64:
    def __init__(self, data: float = 0.0):
        self.data = float(data)

class Bool:
    def __init__(self, data: bool = False):
        self.data = bool(data)


# ==============================================================================
# In-Process Topic Event Bus
# ==============================================================================

class _TopicBus:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(_TopicBus, cls).__new__(cls)
                cls._instance.subscribers: Dict[str, List[Callable[[Any], None]]] = {}
                cls._instance.sub_lock = threading.Lock()
            return cls._instance

    def subscribe(self, topic: str, callback: Callable[[Any], None]):
        with self.sub_lock:
            if topic not in self.subscribers:
                self.subscribers[topic] = []
            self.subscribers[topic].append(callback)

    def unsubscribe(self, topic: str, callback: Callable[[Any], None]):
        with self.sub_lock:
            if topic in self.subscribers and callback in self.subscribers[topic]:
                self.subscribers[topic].remove(callback)

    def publish(self, topic: str, msg: Any):
        with self.sub_lock:
            cbs = list(self.subscribers.get(topic, []))
        for cb in cbs:
            try:
                cb(msg)
            except Exception as e:
                print(f"[TopicBus Error on '{topic}']: {e}")

    def clear(self):
        with self.sub_lock:
            self.subscribers.clear()

topic_bus = _TopicBus()


# ==============================================================================
# Fallback ROS 2 Node & Execution Engine
# ==============================================================================

class _Parameter:
    def __init__(self, name: str, value: Any):
        self.name = name
        self.value = value

class _Logger:
    def __init__(self, name: str):
        self.name = name

    def info(self, msg: str):
        pass  # Quiet in batch runs or print(f"[{self.name}][INFO]: {msg}")

    def warn(self, msg: str):
        print(f"[{self.name}][WARN]: {msg}")

    def error(self, msg: str):
        print(f"[{self.name}][ERROR]: {msg}")

class _Publisher:
    def __init__(self, msg_type: Any, topic: str):
        self.msg_type = msg_type
        self.topic = topic

    def publish(self, msg: Any):
        topic_bus.publish(self.topic, msg)

class _Subscription:
    def __init__(self, msg_type: Any, topic: str, callback: Callable[[Any], None]):
        self.msg_type = msg_type
        self.topic = topic
        self.callback = callback
        topic_bus.subscribe(self.topic, self.callback)

    def destroy(self):
        topic_bus.unsubscribe(self.topic, self.callback)

class _Timer:
    def __init__(self, period_sec: float, callback: Callable[[], None]):
        self.period_sec = period_sec
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def _loop(self):
        while self.running:
            time.sleep(self.period_sec)
            if self.running:
                try:
                    self.callback()
                except Exception as e:
                    print(f"[Timer Error]: {e}")

    def cancel(self):
        self.running = False


class _TimeMsg:
    def __init__(self, sec: int = 0, nanosec: int = 0):
        self.sec = int(sec)
        self.nanosec = int(nanosec)

class _Time:
    def __init__(self, t_sec: float = None):
        if t_sec is None:
            t_sec = time.time()
        self._sec = int(t_sec)
        self._nanosec = int((t_sec - self._sec) * 1e9)

    def to_msg(self) -> _TimeMsg:
        return _TimeMsg(self._sec, self._nanosec)

class _Clock:
    def now(self) -> _Time:
        return _Time(time.time())

class FallbackNode:
    def __init__(self, node_name: str):
        self.node_name = node_name
        self.parameters: Dict[str, _Parameter] = {}
        self.publishers: List[_Publisher] = []
        self.subscriptions: List[_Subscription] = []
        self.timers: List[_Timer] = []
        self._logger = _Logger(node_name)
        self._clock = _Clock()

    def get_clock(self) -> _Clock:
        return self._clock

    def declare_parameter(self, name: str, default_value: Any = None):
        self.parameters[name] = _Parameter(name, default_value)
        return self.parameters[name]

    def get_parameter(self, name: str) -> _Parameter:
        if name not in self.parameters:
            self.declare_parameter(name, None)
        return self.parameters[name]

    def get_logger(self) -> _Logger:
        return self._logger

    def create_publisher(self, msg_type: Any, topic: str, qos_profile: int = 10) -> _Publisher:
        pub = _Publisher(msg_type, topic)
        self.publishers.append(pub)
        return pub

    def create_subscription(self, msg_type: Any, topic: str, callback: Callable[[Any], None], qos_profile: int = 10) -> _Subscription:
        sub = _Subscription(msg_type, topic, callback)
        self.subscriptions.append(sub)
        return sub

    def create_timer(self, period_sec: float, callback: Callable[[], None]) -> _Timer:
        timer = _Timer(period_sec, callback)
        self.timers.append(timer)
        return timer

    def destroy_node(self):
        for timer in self.timers:
            timer.cancel()
        self.timers.clear()
        for sub in self.subscriptions:
            sub.destroy()
        self.subscriptions.clear()
        self.publishers.clear()


# ==============================================================================
# Global Mock rclpy Module & Transparent Injection
# ==============================================================================

class _MockRclpy:
    def __init__(self):
        self._is_initialized = False

    def init(self, args=None):
        self._is_initialized = True

    def shutdown(self):
        self._is_initialized = False
        topic_bus.clear()

    def ok(self) -> bool:
        return self._is_initialized

    def spin(self, node: Any):
        while self._is_initialized:
            time.sleep(0.1)

    def spin_once(self, node: Any, timeout_sec: float = 0.01):
        time.sleep(timeout_sec)

class _MockMultiThreadedExecutor:
    def __init__(self, num_threads: int = 4):
        self.nodes = []

    def add_node(self, node: Any):
        if node not in self.nodes:
            self.nodes.append(node)

    def remove_node(self, node: Any):
        if node in self.nodes:
            self.nodes.remove(node)

    def spin(self):
        time.sleep(0.1)

    def spin_once(self, timeout_sec: float = 0.01):
        time.sleep(timeout_sec)

    def shutdown(self):
        self.nodes.clear()

class _MockSingleThreadedExecutor(_MockMultiThreadedExecutor):
    pass


def install_ros2_shim():
    """
    Transparently installs pure-Python ROS 2 module shims into sys.modules
    if native rclpy is not present. This allows standard 'import rclpy'
    and 'from nav_msgs.msg import Odometry' to work flawlessly on Windows!
    """
    if HAS_NATIVE_ROS2:
        return  # Native ROS 2 exists; do nothing

    import types

    # 1. rclpy
    if 'rclpy' not in sys.modules:
        m_rclpy = _MockRclpy()
        m_rclpy.node = types.ModuleType('rclpy.node')
        m_rclpy.node.Node = FallbackNode
        m_rclpy.executors = types.ModuleType('rclpy.executors')
        m_rclpy.executors.MultiThreadedExecutor = _MockMultiThreadedExecutor
        m_rclpy.executors.SingleThreadedExecutor = _MockSingleThreadedExecutor
        
        sys.modules['rclpy'] = m_rclpy
        sys.modules['rclpy.node'] = m_rclpy.node
        sys.modules['rclpy.executors'] = m_rclpy.executors

    # 2. nav_msgs
    if 'nav_msgs' not in sys.modules:
        m_nav = types.ModuleType('nav_msgs')
        m_nav_msg = types.ModuleType('nav_msgs.msg')
        m_nav_msg.Odometry = Odometry
        m_nav.msg = m_nav_msg
        sys.modules['nav_msgs'] = m_nav
        sys.modules['nav_msgs.msg'] = m_nav_msg

    # 3. geometry_msgs
    if 'geometry_msgs' not in sys.modules:
        m_geo = types.ModuleType('geometry_msgs')
        m_geo_msg = types.ModuleType('geometry_msgs.msg')
        m_geo_msg.Twist = Twist
        m_geo.msg = m_geo_msg
        sys.modules['geometry_msgs'] = m_geo
        sys.modules['geometry_msgs.msg'] = m_geo_msg

    # 4. std_msgs
    if 'std_msgs' not in sys.modules:
        m_std = types.ModuleType('std_msgs')
        m_std_msg = types.ModuleType('std_msgs.msg')
        m_std_msg.Float64MultiArray = Float64MultiArray
        m_std_msg.Int32MultiArray = Int32MultiArray
        m_std_msg.Float64 = Float64
        m_std_msg.Bool = Bool
        m_std.msg = m_std_msg
        sys.modules['std_msgs'] = m_std
        sys.modules['std_msgs.msg'] = m_std_msg

# Automatically install shim on import if native is missing
install_ros2_shim()
