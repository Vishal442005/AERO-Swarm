#!/usr/bin/env python3
"""
AERO-Swarm: ROS 2 Formation Controller Node (aero_formation_controller)
Executes 50 Hz closed-loop consensus guidance by synthesizing:
1. Sheaf Laplacian topological drift setpoints from aero_sheaf_coordinator
2. SHATA mission task navigation vectors from aero_task_allocator
3. Velocity alignment damping to prevent inter-agent oscillations
Publishes raw control setpoints on /drone_{id}/cmd_vel_raw for RTA Simplex interception.
"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray, Int32MultiArray
import numpy as np


class AEROFormationControllerNode(Node):
    def __init__(self, drone_id: int = 0, drone_type: int = 0,
                 kappa_sheaf: float = 0.6, v_max: float = 8.0):
        super().__init__(f'aero_formation_controller_{drone_id}')
        
        self.declare_parameter('drone_id', drone_id)
        self.declare_parameter('drone_type', drone_type)
        self.declare_parameter('kappa_sheaf', kappa_sheaf)
        self.declare_parameter('v_max', v_max)
        
        self.drone_id = drone_id
        self.drone_type = drone_type
        self.kappa_sheaf = kappa_sheaf
        self.v_max = v_max
        
        # State variables
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.sheaf_drift = np.zeros(3)
        self.current_target_pos = None
        self.active_bundle = []
        
        # Publishers and Subscribers
        self.cmd_raw_pub = self.create_publisher(
            Twist, f'/drone_{self.drone_id}/cmd_vel_raw', 10
        )
        
        self.odom_sub = self.create_subscription(
            Odometry, f'/drone_{self.drone_id}/odometry', self.odom_callback, 10
        )
        self.sheaf_drift_sub = self.create_subscription(
            Float64MultiArray, f'/drone_{self.drone_id}/sheaf_drift', self.sheaf_drift_callback, 10
        )
        self.bundle_sub = self.create_subscription(
            Int32MultiArray, f'/drone_{self.drone_id}/assigned_bundle', self.bundle_callback, 10
        )
        
        # 50 Hz control loop (20 ms period - SAE real-time flight loop)
        self.timer = self.create_timer(0.02, self.control_loop)
        self.get_logger().info(f"Initialized AEROFormationControllerNode for Drone {self.drone_id} (50 Hz control loop)")

    def odom_callback(self, msg: Odometry):
        self.pos = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])
        self.vel = np.array([msg.twist.twist.linear.x, msg.twist.twist.linear.y, msg.twist.twist.linear.z])

    def sheaf_drift_callback(self, msg: Float64MultiArray):
        data = list(msg.data)
        if len(data) >= 3:
            self.sheaf_drift = np.array(data[0:3])

    def bundle_callback(self, msg: Int32MultiArray):
        self.active_bundle = list(msg.data)
        if len(self.active_bundle) > 0:
            # Deterministic waypoint calculation for current primary assigned task
            tid = self.active_bundle[0]
            np.random.seed(tid + 100)
            self.current_target_pos = np.array([
                np.random.uniform(-35.0, 35.0),
                np.random.uniform(-35.0, 35.0),
                np.random.uniform(8.0, 22.0)
            ])
        else:
            self.current_target_pos = None

    def control_loop(self):
        # 1. Mission Task Attraction Vector
        u_task = np.zeros(3)
        if self.current_target_pos is not None:
            diff = self.current_target_pos - self.pos
            dist = np.linalg.norm(diff)
            if dist > 0.5:
                direction = diff / dist
                u_task = min(self.v_max * 0.7, 1.2 * dist) * direction
        else:
            # Nominal loiter/patrol orbit if no active task assigned
            orbit_speed = 2.0
            phase = self.drone_id * (2.0 * np.pi / 6.0)
            u_task = np.array([-orbit_speed * np.sin(phase), orbit_speed * np.cos(phase), 0.0])

        # 2. Sheaf Laplacian Consensus Drift Correction
        u_sheaf = -self.kappa_sheaf * self.sheaf_drift

        # 3. Velocity Damping to Prevent Kinetic Ringing
        u_damp = -0.15 * self.vel

        # 4. Synthesize Desired Velocity
        u_des = u_task + u_sheaf + u_damp
        
        # Velocity Saturation Bound
        speed = np.linalg.norm(u_des)
        if speed > self.v_max:
            u_des = (u_des / speed) * self.v_max

        # Publish raw desired velocity command
        cmd_msg = Twist()
        cmd_msg.linear.x = float(u_des[0])
        cmd_msg.linear.y = float(u_des[1])
        cmd_msg.linear.z = float(u_des[2])
        cmd_msg.angular.z = float(np.arctan2(u_des[1], u_des[0] + 1e-5))
        self.cmd_raw_pub.publish(cmd_msg)


def main(args=None):
    rclpy.init(args=args)
    node = AEROFormationControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
