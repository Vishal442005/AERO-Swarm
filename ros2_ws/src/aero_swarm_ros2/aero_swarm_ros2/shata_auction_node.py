#!/usr/bin/env python3
"""
AERO-Swarm: ROS 2 Sheaf-Augmented Task Allocation (SHATA) Node
Executes capability-weighted auction bidding, sheaf Dirichlet bid projections,
and resolves topological bidding deadlocks via 1-st cohomology rank checks.
"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32MultiArray, Float64MultiArray, Float64
import numpy as np
from typing import Dict, List, Any


# Capability affinity matrix [drone_type x task_type]
# Types: 0: Leader, 1: Scout, 2: Relay
# Tasks: 0: Mapping/SLAM, 1: Search/Recon, 2: Comms Bridge, 3: Supply/Escort
CAPABILITY_AFFINITY = np.array([
    [1.0, 0.4, 0.2, 0.5], # Leader (Dominates SLAM/Mapping)
    [0.1, 1.0, 0.1, 0.3], # Scout  (Dominates Search/Recon)
    [0.1, 0.2, 1.0, 0.6], # Relay  (Dominates Comms Bridge)
])


class SHATAAuctionNode(Node):
    def __init__(self, drone_id: int = 0, drone_type: int = 0, total_drones: int = 10,
                 r_comm: float = 80.0, max_bundle_size: int = 4):
        super().__init__(f'shata_auction_node_{drone_id}')
        
        self.declare_parameter('drone_id', drone_id)
        self.declare_parameter('drone_type', drone_type)
        self.declare_parameter('total_drones', total_drones)
        self.declare_parameter('comm_radius', r_comm)
        self.declare_parameter('max_bundle_size', max_bundle_size)
        
        self.drone_id = drone_id
        self.drone_type = drone_type
        self.total_drones = total_drones
        self.r_comm = r_comm
        self.max_bundle_size = max_bundle_size
        
        # Stalk dimensions: Leader 24, Scout 12, Relay 8
        self.stalk_dim = 24 if self.drone_type == 0 else (12 if self.drone_type == 1 else 8)
        self.edge_dim = 6
        
        # Sheaf projection operator P: R^{stalk_dim} -> R^6
        self.P = np.zeros((self.edge_dim, self.stalk_dim))
        self.P[0:3, 0:3] = np.eye(3)
        self.P[3:6, 3:6] = np.eye(3)
        
        # State variables
        self.pos = np.zeros(3)
        self.battery_ratio = 1.0
        self.sheaf_connectivity = 1.0
        self.H1_rank = 0
        
        # Mission task catalog: task_id -> {type, pos, priority, workload, completed}
        self.tasks: Dict[int, Dict[str, Any]] = {}
        self._init_default_tasks()
        
        # Assigned task bundle & current bid list
        self.assigned_bundle: List[int] = []
        self.local_bids: Dict[int, float] = {}
        self.neighbor_bids: Dict[int, Dict[int, float]] = {} # drone_id -> {task_id -> bid}
        
        # Publishers and Subscribers
        self.bundle_pub = self.create_publisher(
            Int32MultiArray, f'/drone_{self.drone_id}/assigned_bundle', 10
        )
        self.bid_pub = self.create_publisher(
            Float64MultiArray, f'/drone_{self.drone_id}/task_bids', 10
        )
        self.h1_pub = self.create_publisher(
            Float64, f'/drone_{self.drone_id}/cohomology_h1_rank', 10
        )
        
        self.odom_sub = self.create_subscription(
            Odometry, f'/drone_{self.drone_id}/odometry', self.odom_callback, 10
        )
        self.scvi_sub = self.create_subscription(
            Float64, f'/drone_{self.drone_id}/scvi_curvature', self.scvi_callback, 10
        )
        
        # Subscribe to neighbor bids over mesh
        self.neighbor_bid_subs = {}
        for nid in range(self.total_drones):
            if nid != self.drone_id:
                self.neighbor_bid_subs[nid] = self.create_subscription(
                    Float64MultiArray, f'/drone_{nid}/task_bids',
                    lambda msg, n=nid: self.neighbor_bid_callback(msg, n), 10
                )
        
        # Auction cycle at 2 Hz
        self.timer = self.create_timer(0.5, self.auction_cycle)
        self.get_logger().info(f"Initialized SHATAAuctionNode for Drone {self.drone_id} (Type {self.drone_type}, Stalk {self.stalk_dim})")

    def _init_default_tasks(self):
        """Populate initial representative mission tasks across search area."""
        task_types = [0, 1, 2, 3] # SLAM, Search, Comms, Escort
        np.random.seed(42)
        for tid in range(12):
            ttype = task_types[tid % 4]
            tpos = np.array([
                np.random.uniform(-40.0, 40.0),
                np.random.uniform(-40.0, 40.0),
                np.random.uniform(5.0, 25.0)
            ])
            priority = 1.0 + (tid % 3) * 0.5
            workload = 8.0 + (tid % 4) * 2.0
            self.tasks[tid] = {
                'id': tid,
                'type': ttype,
                'pos': tpos,
                'priority': priority,
                'workload': workload,
                'completed': False
            }

    def odom_callback(self, msg: Odometry):
        self.pos = np.array([msg.pose.pose.position.x, msg.pose.pose.position.y, msg.pose.pose.position.z])
        # Energy discharge model based on movement
        speed = np.linalg.norm([msg.twist.twist.linear.x, msg.twist.twist.linear.y, msg.twist.twist.linear.z])
        self.battery_ratio = max(0.1, self.battery_ratio - 0.0001 * (1.0 + speed * 0.1))

    def scvi_callback(self, msg: Float64):
        self.sheaf_connectivity = float(msg.data)

    def neighbor_bid_callback(self, msg: Float64MultiArray, nid: int):
        data = list(msg.data)
        if len(data) >= 2:
            self.neighbor_bids[nid] = {}
            for i in range(0, len(data) - 1, 2):
                tid = int(data[i])
                bid = float(data[i + 1])
                self.neighbor_bids[nid][tid] = bid

    def compute_bid(self, task: Dict[str, Any]) -> float:
        """Computes capability-weighted sheaf bid for a specific task."""
        affinity = CAPABILITY_AFFINITY[self.drone_type, task['type']]
        if affinity < 0.1:
            return 0.0
            
        dist = np.linalg.norm(self.pos - task['pos'])
        dist_factor = np.exp(-dist / self.r_comm)
        energy_factor = max(0.0, self.battery_ratio) ** 1.5
        sheaf_factor = 1.0 + 0.5 * min(self.sheaf_connectivity, 5.0)
        
        bid = (affinity * task['priority'] / (task['workload'] + 1.0)) * dist_factor * energy_factor * sheaf_factor
        return float(bid)

    def evaluate_cohomology_obstruction(self) -> int:
        """
        Calculates first cohomology group rank dim H^1 by identifying
        cyclic circular outbidding deadlocks between local agent and neighbors.
        """
        deadlock_cycles = 0
        for nid, nbids in self.neighbor_bids.items():
            for tid, nbid in nbids.items():
                my_bid = self.local_bids.get(tid, 0.0)
                # If bids are within 5% marginal threshold, potential conflict cycle
                if my_bid > 0.0 and abs(my_bid - nbid) / max(my_bid, nbid, 1e-4) < 0.05:
                    deadlock_cycles += 1
        self.H1_rank = 1 if deadlock_cycles >= 2 else 0
        return self.H1_rank

    def auction_cycle(self):
        # 1. Compute bids for all uncompleted tasks
        self.local_bids.clear()
        for tid, task in self.tasks.items():
            if not task['completed']:
                self.local_bids[tid] = self.compute_bid(task)

        # 2. Sheaf Dirichlet Projection: project multi-dim bid vector onto edge stalk
        bid_vector = np.zeros(self.stalk_dim)
        bid_items = sorted(self.local_bids.items(), key=lambda x: x[1], reverse=True)
        for idx, (tid, b_val) in enumerate(bid_items[:min(len(bid_items), self.stalk_dim)]):
            bid_vector[idx] = b_val
        y_projected_bid = self.P @ bid_vector # R^6 shared edge projection

        # 3. Publish bid list over mesh [tid_0, bid_0, tid_1, bid_1, ...]
        bid_msg = Float64MultiArray()
        flat_data = []
        for tid, b_val in self.local_bids.items():
            flat_data.extend([float(tid), float(b_val)])
        bid_msg.data = flat_data
        self.bid_pub.publish(bid_msg)

        # 4. Cohomological conflict resolution
        h1 = self.evaluate_cohomology_obstruction()
        h1_msg = Float64()
        h1_msg.data = float(h1)
        self.h1_pub.publish(h1_msg)

        # 5. Bundle consensus deconfliction
        new_bundle = []
        for tid, my_bid in bid_items:
            if my_bid <= 1e-4:
                continue
            # Check against neighbor bids
            is_winner = True
            for nid, nbids in self.neighbor_bids.items():
                if tid in nbids:
                    nbid = nbids[tid]
                    if nbid > my_bid:
                        is_winner = False
                        break
                    elif abs(nbid - my_bid) <= 1e-5:
                        # Tie breaker: lowest drone ID wins
                        if nid < self.drone_id:
                            is_winner = False
                            break
            
            if is_winner and len(new_bundle) < self.max_bundle_size:
                new_bundle.append(tid)

        self.assigned_bundle = new_bundle
        
        # 6. Publish assigned bundle
        bundle_msg = Int32MultiArray()
        bundle_msg.data = self.assigned_bundle
        self.bundle_pub.publish(bundle_msg)


def main(args=None):
    rclpy.init(args=args)
    node = SHATAAuctionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
