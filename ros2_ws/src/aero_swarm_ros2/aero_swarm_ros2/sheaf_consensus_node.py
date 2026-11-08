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
        
        # Stalk dimensions: Leader 24, Scout 12, Relay 8 (per SWEVO archival specification)
        self.stalk_dim = 24 if self.drone_type == 0 else (12 if self.drone_type == 1 else 8)
        self.edge_dim = 6
        
        # Base orthogonal projection matrix P_v: R^{stalk_dim} -> R^6 (3D Pos + 3D Vel)
        self.P_base = np.zeros((self.edge_dim, self.stalk_dim))
        self.P_base[0:3, 0:3] = np.eye(3)
        self.P_base[3:6, 3:6] = np.eye(3)
        self.P = np.copy(self.P_base)
        
        # State vector x_i in R^{stalk_dim}
        self.x_local = np.zeros(self.stalk_dim)
        
        # Link channel quality gamma_e(t) in [0, 1]
        self.link_gammas = {nid: 1.0 for nid in range(self.total_drones)}
        
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
        self.sheaf_drift_pub = self.create_publisher(
            Float64MultiArray, f'/drone_{self.drone_id}/sheaf_drift', 10
        )
        self.scvi_pub = self.create_publisher(
            Float64, f'/drone_{self.drone_id}/scvi_curvature', 10
        )
        self.rf_gamma_sub = self.create_subscription(
            Float64MultiArray, f'/drone_{self.drone_id}/rf_link_gamma', self.rf_gamma_callback, 10
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

    def rf_gamma_callback(self, msg: Float64MultiArray):
        data = list(msg.data)
        for i in range(0, len(data) - 1, 2):
            nid = int(data[i])
            gamma_val = float(data[i + 1])
            self.link_gammas[nid] = np.clip(gamma_val, 0.01, 1.0)

    def neighbor_sheaf_callback(self, msg: Float64MultiArray, nid: int):
        self.neighbor_sheaf_states[nid] = np.array(msg.data)

    def consensus_cycle(self):
        # 1. Update dynamic restriction map with mean channel attenuation
        mean_gamma = float(np.mean(list(self.link_gammas.values()))) if self.link_gammas else 1.0
        self.P = np.sqrt(mean_gamma) * self.P_base
        
        # 2. Project local stalk to edge stalk: y_i = rho_{v \trianglelefteq e} x_local
        y_i = self.P @ self.x_local
        
        # 3. Publish projected cochain
        msg = Float64MultiArray()
        msg.data = y_i.tolist()
        self.sheaf_state_pub.publish(msg)
        
        # 4. Sheaf Laplacian cochain drift:
        # (\mathcal{L}_\mathcal{F} x)_v = \sum_{j \in N_v} rho_{v \trianglelefteq e}^T (rho_{v \trianglelefteq e} x_v - rho_{u \trianglelefteq e} x_u)
        sheaf_drift = np.zeros(self.stalk_dim)
        if len(self.neighbor_sheaf_states) > 0:
            count = 0
            for nid, y_j in list(self.neighbor_sheaf_states.items()):
                gamma_e = self.link_gammas.get(nid, 1.0)
                # Weighted edge restriction map
                rho_ve = np.sqrt(gamma_e) * self.P_base
                diff_e = y_i - y_j[:self.edge_dim]
                sheaf_drift += rho_ve.T @ diff_e
                count += 1
                
            if count > 0:
                dt = 0.05
                self.x_local -= (self.gamma_gain / count) * sheaf_drift * dt
        
        # Publish sheaf drift for formation controller
        drift_msg = Float64MultiArray()
        drift_msg.data = sheaf_drift.tolist()
        self.sheaf_drift_pub.publish(drift_msg)
        
        # 5. Forman-Ricci curvature (SCVI) computation: trace(rho^T rho)
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
