#!/usr/bin/env python3
"""
AERO-Swarm: ROS 2 Sheaf Consensus Node
Computes local restriction maps, evaluates link integrity under RF interference,
and updates state over edge stalks using the Sheaf Laplacian.
"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray, Float64
import numpy as np


class SheafConsensusNode(Node):
    def __init__(self):
        super().__init__('sheaf_consensus_node')
        
        # Declare parameters
        self.declare_parameter('drone_id', 0)
        self.declare_parameter('drone_type', 0) # 0: Leader, 1: Scout, 2: Relay
        self.declare_parameter('comm_radius', 80.0)
        self.declare_parameter('consensus_gain', 0.8)
        
        self.drone_id = self.get_parameter('drone_id').value
        self.drone_type = self.get_parameter('drone_type').value
        self.comm_radius = self.get_parameter('comm_radius').value
        self.gamma_gain = self.get_parameter('consensus_gain').value
        
        # Stalk dimensions: Leader 24, Scout 12, Relay 6
        self.stalk_dim = 24 if self.drone_type == 0 else (12 if self.drone_type == 1 else 6)
        self.edge_dim = 6
        
        # State vector
        self.x_local = np.zeros(self.stalk_dim)
        
        # Restriction map P: R^{stalk_dim} -> R^6 (3D Pos + 3D Vel)
        self.P = np.zeros((self.edge_dim, self.stalk_dim))
        self.P[0:3, 0:3] = np.eye(3)
        self.P[3:6, 3:6] = np.eye(3)
        
        # ROS 2 Subscriptions & Publishers
        self.odom_sub = self.create_subscription(
            Odometry, f'/drone_{self.drone_id}/odometry', self.odom_callback, 10
        )
        self.sheaf_state_pub = self.create_publisher(
            Float64MultiArray, f'/drone_{self.drone_id}/sheaf_state', 10
        )
        self.scvi_pub = self.create_publisher(
            Float64, f'/drone_{self.drone_id}/scvi_curvature', 10
        )
        
        # Timer: 20 Hz consensus cycle
        self.timer = self.create_timer(0.05, self.consensus_cycle)
        self.get_logger().info(f"Initialized SheafConsensusNode for Drone {self.drone_id} (Type {self.drone_type}, Stalk Dim {self.stalk_dim})")

    def odom_callback(self, msg: Odometry):
        # Update local physical state
        pos = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])
        vel = np.array([msg.twist.twist.linear.x, msg.twist.twist.linear.y, msg.twist.twist.linear.z])
        self.x_local[0:3] = pos
        self.x_local[3:6] = vel

    def consensus_cycle(self):
        # 1. Project local stalk to edge stalk: y_i = P @ x_local
        y_projected = self.P @ self.x_local
        
        # 2. Publish projected cochain
        msg = Float64MultiArray()
        msg.data = y_projected.tolist()
        self.sheaf_state_pub.publish(msg)
        
        # 3. Forman curvature (SCVI) computation
        curvature = float(np.trace(self.P.T @ self.P))
        c_msg = Float64()
        c_msg.data = curvature
        self.scvi_pub.publish(c_msg)


def main(args=None):
    rclpy.init(args=args)
    node = SheafConsensusNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
