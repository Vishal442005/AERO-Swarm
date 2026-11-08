#!/usr/bin/env python3
"""
AERO-Swarm: ROS 2 Swarm World Simulation & Telemetry Node
Maintains ground-truth continuous 3D quadrotor dynamics, publishes odometry,
evaluates inter-drone physical distances, monitors communication latency,
and records comprehensive real-time telemetry.
"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64MultiArray, Bool
import numpy as np
import time


class SwarmWorldSimNode(Node):
    def __init__(self, num_drones: int = 10, d_safe: float = 2.5, sim_step_dt: float = 0.02):
        super().__init__('swarm_world_sim_node')
        
        self.declare_parameter('num_drones', num_drones)
        self.declare_parameter('d_safe', d_safe)
        self.declare_parameter('sim_step_dt', sim_step_dt)
        
        self.num_drones = num_drones
        self.d_safe = d_safe
        self.dt = sim_step_dt
        
        # State: positions and velocities
        # Heterogeneity: 20% Leaders (0), 60% Scouts (1), 20% Relays (2)
        n_lead = max(1, int(self.num_drones * 0.2))
        n_relay = max(1, int(self.num_drones * 0.2))
        n_scout = self.num_drones - n_lead - n_relay
        
        self.drone_types = [0] * n_lead + [1] * n_scout + [2] * n_relay
        np.random.shuffle(self.drone_types)
        
        # Spawn drones ensuring minimum separation >= d_safe + 1.5m
        self.positions = np.zeros((self.num_drones, 3))
        self.velocities = np.zeros((self.num_drones, 3))
        self.safe_cmds = np.zeros((self.num_drones, 3))
        
        placed = 0
        attempts = 0
        while placed < self.num_drones and attempts < 10000:
            cand = np.array([
                np.random.uniform(-40.0, 40.0),
                np.random.uniform(-40.0, 40.0),
                np.random.uniform(10.0, 30.0)
            ])
            too_close = False
            for p in range(placed):
                if np.linalg.norm(cand - self.positions[p]) < self.d_safe + 1.5:
                    too_close = True
                    break
            if not too_close:
                self.positions[placed] = cand
                placed += 1
            attempts += 1
            
        # Telemetry metrics
        self.metrics = {
            'total_odom_published': 0,
            'total_mesh_tx_received': 0,
            'total_sheaf_cochains_received': 0,
            'min_inter_drone_distance': 999.0,
            'safety_violations': 0,
            'latency_samples_ms': [],
            'step_count': 0
        }
        
        # Publishers for odometry
        self.odom_pubs = {}
        self.raw_cmd_pubs = {}
        for i in range(self.num_drones):
            self.odom_pubs[i] = self.create_publisher(
                Odometry, f'/drone_{i}/odometry', 10
            )
            self.raw_cmd_pubs[i] = self.create_publisher(
                Twist, f'/drone_{i}/cmd_vel_raw', 10
            )
            
        # Subscriptions for safe commands and mesh transmissions
        self.safe_cmd_subs = {}
        self.mesh_tx_subs = {}
        self.sheaf_subs = {}
        for i in range(self.num_drones):
            # Capture loop variable i via default argument
            self.safe_cmd_subs[i] = self.create_subscription(
                Twist, f'/drone_{i}/cmd_vel_safe',
                lambda msg, drone_idx=i: self.safe_cmd_callback(msg, drone_idx), 10
            )
            self.mesh_tx_subs[i] = self.create_subscription(
                Float64MultiArray, f'/drone_{i}/mesh_tx',
                lambda msg, drone_idx=i: self.mesh_tx_callback(msg, drone_idx), 10
            )
            self.sheaf_subs[i] = self.create_subscription(
                Float64MultiArray, f'/drone_{i}/sheaf_state',
                lambda msg, drone_idx=i: self.sheaf_state_callback(msg, drone_idx), 10
            )
            
        # Simulation loop timer (50 Hz)
        self.timer = self.create_timer(self.dt, self.physics_step)
        self.get_logger().info(f"Initialized SwarmWorldSimNode for {self.num_drones} heterogeneous UAVs.")

    def safe_cmd_callback(self, msg: Twist, drone_idx: int):
        self.safe_cmds[drone_idx] = [msg.linear.x, msg.linear.y, msg.linear.z]

    def mesh_tx_callback(self, msg: Float64MultiArray, drone_idx: int):
        self.metrics['total_mesh_tx_received'] += 1

    def sheaf_state_callback(self, msg: Float64MultiArray, drone_idx: int):
        self.metrics['total_sheaf_cochains_received'] += 1

    def physics_step(self):
        t_start = time.perf_counter()
        self.metrics['step_count'] += 1
        
        # 1. Update quadrotor velocities and positions
        for i in range(self.num_drones):
            # Simple second-order drag dynamics: v_dot = (u_cmd - v) / tau
            tau = 0.2
            self.velocities[i] += ((self.safe_cmds[i] - self.velocities[i]) / tau) * self.dt
            self.positions[i] += self.velocities[i] * self.dt
            
            # Ground boundary clamp
            if self.positions[i, 2] < 1.0:
                self.positions[i, 2] = 1.0
                self.velocities[i, 2] = 0.0

        # 2. Check all pairwise distances for CBF Safety Invariance
        for i in range(self.num_drones):
            for j in range(i + 1, self.num_drones):
                dist = float(np.linalg.norm(self.positions[i] - self.positions[j]))
                if dist < self.metrics['min_inter_drone_distance']:
                    self.metrics['min_inter_drone_distance'] = dist
                if dist < self.d_safe - 1e-3: # Violation tolerance
                    self.metrics['safety_violations'] += 1

        # 3. Publish Odometry and synthetic goal seeking cmd_vel_raw
        ros_time = self.get_clock().now().to_msg()
        for i in range(self.num_drones):
            # Publish Odometry
            odom_msg = Odometry()
            odom_msg.header.stamp = ros_time
            odom_msg.header.frame_id = 'world'
            odom_msg.child_frame_id = f'drone_{i}'
            odom_msg.pose.pose.position.x = float(self.positions[i, 0])
            odom_msg.pose.pose.position.y = float(self.positions[i, 1])
            odom_msg.pose.pose.position.z = float(self.positions[i, 2])
            odom_msg.twist.twist.linear.x = float(self.velocities[i, 0])
            odom_msg.twist.twist.linear.y = float(self.velocities[i, 1])
            odom_msg.twist.twist.linear.z = float(self.velocities[i, 2])
            self.odom_pubs[i].publish(odom_msg)
            self.metrics['total_odom_published'] += 1
            
            # Send desired raw command (slight centripetal flocking pull)
            center = np.mean(self.positions, axis=0)
            u_dir = center - self.positions[i]
            dist_c = np.linalg.norm(u_dir)
            if dist_c > 1e-3:
                u_dir = (u_dir / dist_c) * 1.5
            else:
                u_dir = np.zeros(3)
                
            raw_cmd = Twist()
            raw_cmd.linear.x = float(u_dir[0])
            raw_cmd.linear.y = float(u_dir[1])
            raw_cmd.linear.z = float(u_dir[2])
            self.raw_cmd_pubs[i].publish(raw_cmd)
            
        t_elapsed_ms = (time.perf_counter() - t_start) * 1000.0
        self.metrics['latency_samples_ms'].append(t_elapsed_ms)


def main(args=None):
    rclpy.init(args=args)
    node = SwarmWorldSimNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
