#!/usr/bin/env python3
"""
AERO-Swarm: ROS 2 Information-Geometric Event-Triggered Communication (IG-ETC) Node
Computes the Fisher-Rao Riemannian distance between Gaussian belief states
and triggers mesh broadcast only when d_FR exceeds the energy-annealed threshold.
"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray, Bool
import numpy as np
import scipy.linalg as la


class IGETCTriggerNode(Node):
    def __init__(self):
        super().__init__('ig_etc_trigger_node')
        
        self.declare_parameter('drone_id', 0)
        self.declare_parameter('delta_min', 0.4)
        self.declare_parameter('delta_max', 2.5)
        self.declare_parameter('beta_energy', 2.0)
        
        self.drone_id = self.get_parameter('drone_id').value
        self.delta_min = self.get_parameter('delta_min').value
        self.delta_max = self.get_parameter('delta_max').value
        self.beta_energy = self.get_parameter('beta_energy').value
        
        # Gaussian Belief: p(t) = N(mu, Sigma)
        self.mu_curr = np.zeros(6) # 3D Pos + 3D Vel
        self.Sigma_curr = np.eye(6) * 0.05
        
        # Last Broadcast Belief
        self.mu_last = np.zeros(6)
        self.Sigma_last = np.eye(6) * 0.05
        
        self.battery_ratio = 1.0
        self.mean_link_gamma = 1.0
        
        # Subscribers & Publishers
        self.odom_sub = self.create_subscription(
            Odometry, f'/drone_{self.drone_id}/odometry', self.odom_callback, 10
        )
        self.broadcast_pub = self.create_publisher(
            Float64MultiArray, f'/drone_{self.drone_id}/mesh_tx', 10
        )
        self.trigger_status_pub = self.create_publisher(
            Bool, f'/drone_{self.drone_id}/ig_trigger_active', 10
        )
        
        # High-frequency trigger check (50 Hz)
        self.timer = self.create_timer(0.02, self.check_trigger)
        self.get_logger().info(f"Initialized IGETCTriggerNode for Drone {self.drone_id}")

    def odom_callback(self, msg: Odometry):
        self.mu_curr[0:3] = [msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z]
        self.mu_curr[3:6] = [msg.twist.twist.linear.x, msg.twist.twist.linear.y, msg.twist.twist.linear.z]
        # Inflate covariance slightly on motion
        self.Sigma_curr[0:3, 0:3] += np.eye(3) * 0.001

    def compute_fisher_rao_distance(self) -> float:
        """Computes Riemannian geodesic distance on Gaussian manifold."""
        eps = 1e-5
        S1 = self.Sigma_curr + eps * np.eye(6)
        S2 = self.Sigma_last + eps * np.eye(6)
        try:
            eigenvals = la.eigvals(S1, S2).real
            eigenvals = np.clip(eigenvals, 1e-6, 1e6)
            log_term = 0.5 * np.sum(np.log(eigenvals) ** 2)
            
            S_mid = 0.5 * (S1 + S2)
            diff = self.mu_curr - self.mu_last
            mahalanobis = diff.T @ la.solve(S_mid, diff)
            return float(np.sqrt(max(0.0, log_term + mahalanobis)))
        except Exception:
            return float(np.linalg.norm(self.mu_curr - self.mu_last))

    def check_trigger(self):
        d_FR = self.compute_fisher_rao_distance()
        
        # Energy annealed threshold: delta_i(E)
        delta_i = self.delta_min + (self.delta_max - self.delta_min) * np.exp(-self.beta_energy * self.battery_ratio)
        
        status_msg = Bool()
        if d_FR > delta_i:
            # Event triggered! Broadcast packet over mesh
            status_msg.data = True
            msg = Float64MultiArray()
            msg.data = self.mu_curr.tolist()
            self.broadcast_pub.publish(msg)
            
            # Update last acknowledged belief
            self.mu_last = np.copy(self.mu_curr)
            self.Sigma_last = np.copy(self.Sigma_curr)
        else:
            status_msg.data = False
            
        self.trigger_status_pub.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    node = IGETCTriggerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
