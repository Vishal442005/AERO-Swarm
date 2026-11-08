import sys
import os

# Add ros2_ws/src/aero_swarm_ros2 and src to Python path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ros2_pkg = os.path.join(repo_root, 'ros2_ws', 'src', 'aero_swarm_ros2')
src_dir = os.path.join(repo_root, 'src')

if ros2_pkg not in sys.path:
    sys.path.insert(0, ros2_pkg)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Initialize ROS 2 bridge for headless / Windows execution
import aero_swarm_ros2.ros2_bridge
