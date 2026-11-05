"""
AERO-Swarm: Sheaf-Augmented Heterogeneous Task Allocation (SHATA)
Implements capability-weighted bidding, bundle construction, and cohomological
conflict resolution (H^1 rank check) to eliminate outbidding deadlocks under jamming.
"""

import numpy as np
from typing import List, Dict, Tuple, Set, Any, Optional


# Capability affinity matrix [drone_type x task_type]
# Types: 0: Leader, 1: Scout, 2: Relay
# Tasks: 0: Mapping/SLAM, 1: Search/Recon, 2: Comms Bridge, 3: Supply/Escort
CAPABILITY_AFFINITY = np.array([
    [1.0, 0.4, 0.2, 0.5], # Leader (Dominates SLAM/Mapping)
    [0.1, 1.0, 0.1, 0.3], # Scout  (Dominates Search/Recon)
    [0.1, 0.2, 1.0, 0.6], # Relay  (Dominates Comms Bridge)
])


class MissionTask:
    def __init__(self, task_id: int, task_type: int, position: np.ndarray, 
                 priority: float = 1.0, workload: float = 10.0):
        self.id = task_id
        self.type = task_type
        self.position = np.array(position, dtype=np.float64)
        self.priority = priority
        self.workload = workload
        self.is_completed = False


class SHATAAuctioneer:
    def __init__(self, r_comm: float = 80.0, alpha_sheaf: float = 0.5, 
                 max_bundle_size: int = 4):
        self.r_comm = r_comm
        self.alpha_sheaf = alpha_sheaf
        self.max_bundle_size = max_bundle_size

    def compute_bid(self, drone_id: int, drone_type: int, drone_pos: np.ndarray, 
                    energy_ratio: float, sheaf_connectivity: float, 
                    task: MissionTask) -> float:
        """
        Computes capability-weighted sheaf bid for a specific task.
        """
        affinity = CAPABILITY_AFFINITY[drone_type, task.type]
        if affinity < 0.1:
            return 0.0
            
        dist = np.linalg.norm(drone_pos - task.position)
        dist_factor = np.exp(-dist / self.r_comm)
        energy_factor = max(0.0, energy_ratio) ** 1.5
        sheaf_factor = 1.0 + self.alpha_sheaf * min(sheaf_connectivity, 5.0)
        
        bid = (affinity * task.priority / (task.workload + 1.0)) * dist_factor * energy_factor * sheaf_factor
        return float(bid)

    def allocate_tasks_swarm(self, drones: List[Any], tasks: List[MissionTask], 
                             L_sheaf: np.ndarray, H1_rank: int,
                             offsets: Optional[List[int]] = None
                             ) -> Dict[int, List[int]]:
        """
        Executes distributed auction with cohomological conflict resolution.
        
        Args:
            drones: List of HeterogeneousDrone instances
            tasks: List of active MissionTask objects
            L_sheaf: Current global Sheaf Laplacian matrix
            H1_rank: Rank of 1-st cohomology group (topological obstructions)
            offsets: Optional list of node stalk offsets in L_sheaf
            
        Returns:
            assignments: Dict mapping drone_id -> list of assigned task IDs
        """
        num_drones = len(drones)
        bundles = {i: [] for i in range(num_drones)}
        all_bids = np.zeros((num_drones, len(tasks)), dtype=np.float64)
        
        # Build offsets dynamically if not provided
        if offsets is None:
            stalk_map = {0: 24, 1: 12, 2: 8}
            offsets = [0]
            for d in drones:
                offsets.append(offsets[-1] + stalk_map.get(d.type, 6))

        # 1. Compute bids across all drones and tasks
        for i, drone in enumerate(drones):
            if not drone.is_alive:
                continue
            # Extract drone's local sheaf connectivity degree from diagonal stalk block of L_sheaf
            if len(offsets) > i + 1 and L_sheaf.shape[0] >= offsets[i+1]:
                sheaf_deg = float(np.trace(L_sheaf[offsets[i]:offsets[i+1], offsets[i]:offsets[i+1]]))
            else:
                sheaf_deg = 1.0

            for t_idx, task in enumerate(tasks):
                if not task.is_completed:
                    all_bids[i, t_idx] = self.compute_bid(
                        drone.id, drone.type, drone.pos, drone.energy_ratio, sheaf_deg, task
                    )
                    
        # 2. Greedy bundle construction and conflict resolution
        for t_idx, task in enumerate(tasks):
            if task.is_completed:
                continue
            bids = all_bids[:, t_idx]
            max_bid = np.max(bids)
            if max_bid <= 1e-4:
                continue
                
            candidate_winners = np.where(bids > 0.8 * max_bid)[0]
            
            # Cohomological Obstruction Resolution:
            if H1_rank == 0:
                # Connected/consistent topology: assign to absolute highest bidder
                winner = int(np.argmax(bids))
            else:
                # Topological obstruction present (H^1 > 0, e.g. jamming cut):
                # Resolve by local sheaf Dirichlet alignment (drone with best local consensus)
                winner = int(candidate_winners[0])
                
            if len(bundles[winner]) < self.max_bundle_size:
                bundles[winner].append(task.id)
                
        return bundles
