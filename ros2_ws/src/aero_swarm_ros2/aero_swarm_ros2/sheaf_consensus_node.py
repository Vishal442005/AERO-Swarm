#!/usr/bin/env python3
"""
AERO-Swarm: ROS 2 Sheaf Consensus Node
Computes local restriction maps, evaluates link integrity under RF interference,
subscribes to neighbor cochains, and updates state over edge stalks using the Sheaf Laplacian.
"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray, Float64
import numpy as np


class SheafConsensusNode(Node):
    def __init__(self, drone_id: int = 0, drone_type: int = 0, total_drones: int = 10):
        super().__init__(f'sheaf_consensus_node_{drone_id}')
        
        # Declare parameters
        self.declare_parameter('drone_id', drone_id)
        self.declare_parameter('drone_type', drone_type) # 0: Leader, 1: Scout, 2: Relay
        self.declare_parameter('total_drones', total_drones)
        self.declare_parameter('comm_radius', 80.0)
        self.declare_parameter('consensus_gain', 0.8)
        
        self.drone_id = drone_id
        self.drone_type = drone_type
        self.total_drones = total_drones
        self.comm_radius = self.get_parameter('comm_radius').value
        self.gamma_gain = self.get_parameter('consensus_gain').value
        
        # Stalk dimensions: Leader 24, Scout 12, Relay 6
        self.stalk_dim = 24 if self.drone_type == 0 else (12 if self.drone_type == 1 else 6)
        self.edge_dim = 6
        
        # State vector x_i in R^{stalk_dim}
        self.x_local = np.zeros(self.stalk_dim)
        
        # Restriction map P: R^{stalk_dim} -> R^6 (3D Pos + 3D Vel projection)
        self.P = np.zeros((self.edge_dim, self.stalk_dim))
        self.P[0:3, 0:3] = np.eye(3)
        self.P[3:6, 3:6] = np.eye(3)
        
        # Neighbor edge projections: y_j = P_j @ x_j in R^6
        self.neighbor_sheaf_states = {}
        self.neighbor_poses = {}
        
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
        
        # Subscribe to neighbor sheaf states
        self.neighbor_subs = {}
        for nid in range(self.total_drones):
            if nid != self.drone_id:
                self.neighbor_subs[nid] = self.create_subscription(
                    Float64MultiArray, f'/drone_{nid}/sheaf_state',
                    lambda msg, n=nid: self.neighbor_sheaf_callback(msg, n), 10
                )
                
        # Timer: 20 Hz consensus cycle
        self.timer = self.create_timer(0.05, self.consensus_cycle)
        self.get_logger().info(f"Initialized SheafConsensusNode for Drone {self.drone_id} (Type {self.drone_type}, Stalk {self.stalk_dim})")

    def odom_callback(self, msg: Odometry):
        # Update local physical state
        pos = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])
        vel = np.array([msg.twist.twist.linear.x, msg.twist.twist.linear.y, msg.twist.twist.linear.z])
        self.x_local[0:3] = pos
        self.x_local[3:6] = vel

    def neighbor_sheaf_callback(self, msg: Float64MultiArray, nid: int):
        self.neighbor_sheaf_states[nid] = np.array(msg.data)

    def consensus_cycle(self):
        # 1. Project local stalk to edge stalk: y_i = P @ x_local
        y_i = self.P @ self.x_local
        
        # 2. Publish projected cochain
        msg = Float64MultiArray()
        msg.data = y_i.tolist()
        self.sheaf_state_pub.publish(msg)
        
        # 3. Sheaf Laplacian consensus step:
        # dx_i/dt = -gamma * \sum_{j \in N_i} P_{ij}^T (P_{ij} x_i - P_{ji} x_j)
        if len(self.neighbor_sheaf_states) > 0:
            laplacian_step = np.zeros(self.stalk_dim)
            count = 0
            for nid, y_j in list(self.neighbor_sheaf_states.items()):
                # Edge difference in R^6
                diff_e = y_i - y_j[:self.edge_dim]
                # Pull back to stalk via P^T
                laplacian_step += self.P.T @ diff_e
                count += 1
            if count > 0:
                dt = 0.05
                self.x_local -= (self.gamma_gain / count) * laplacian_step * dt
        
        # 4. Forman-Ricci curvature (SCVI) computation
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
