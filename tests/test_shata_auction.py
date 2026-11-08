"""
Unit tests for SHATA (Sheaf-Augmented Heterogeneous Task Allocation)
"""

import pytest
import numpy as np
from src.auction.shata import SHATAAuctioneer, MissionTask, CAPABILITY_AFFINITY
from src.core.sheaf import DroneType
from src.core.quadrotor_dynamics import HeterogeneousDrone


def test_capability_affinity():
    # Leader dominates mapping (type 0)
    assert CAPABILITY_AFFINITY[DroneType.LEADER, 0] > CAPABILITY_AFFINITY[DroneType.SCOUT, 0]
    # Scout dominates recon (type 1)
    assert CAPABILITY_AFFINITY[DroneType.SCOUT, 1] > CAPABILITY_AFFINITY[DroneType.LEADER, 1]
    # Relay dominates comms bridge (type 2)
    assert CAPABILITY_AFFINITY[DroneType.RELAY, 2] > CAPABILITY_AFFINITY[DroneType.SCOUT, 2]


def test_shata_bid_computation():
    auctioneer = SHATAAuctioneer(r_comm=80.0)
    task = MissionTask(task_id=0, task_type=1, position=np.array([10.0, 10.0, 10.0]), priority=2.0)
    
    # Scout close to task with full battery
    bid_scout = auctioneer.compute_bid(
        drone_id=1,
        drone_type=DroneType.SCOUT,
        drone_pos=np.array([12.0, 10.0, 10.0]),
        energy_ratio=1.0,
        sheaf_connectivity=2.0,
        task=task
    )
    
    # Leader far away with low battery
    bid_leader = auctioneer.compute_bid(
        drone_id=0,
        drone_type=DroneType.LEADER,
        drone_pos=np.array([70.0, 70.0, 10.0]),
        energy_ratio=0.2,
        sheaf_connectivity=1.0,
        task=task
    )
    
    assert bid_scout > bid_leader
    assert bid_scout > 0.0


def test_shata_allocation():
    auctioneer = SHATAAuctioneer(r_comm=80.0)
    
    d1 = HeterogeneousDrone(0, DroneType.LEADER, np.array([0.0, 0.0, 10.0]))
    d2 = HeterogeneousDrone(1, DroneType.SCOUT, np.array([10.0, 0.0, 10.0]))
    d3 = HeterogeneousDrone(2, DroneType.RELAY, np.array([20.0, 0.0, 10.0]))
    drones = [d1, d2, d3]
    
    tasks = [
        MissionTask(0, 0, np.array([1.0, 1.0, 10.0])), # SLAM task near Leader
        MissionTask(1, 1, np.array([11.0, 1.0, 10.0])), # Recon task near Scout
        MissionTask(2, 2, np.array([21.0, 1.0, 10.0]))  # Comms task near Relay
    ]
    
    L_dummy = np.eye(24 + 12 + 8)
    assignments = auctioneer.allocate_tasks_swarm(drones, tasks, L_dummy, H1_rank=0)
    
    assert isinstance(assignments, dict)
    assert len(assignments) == 3
