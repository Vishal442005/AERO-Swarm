"""
Unit tests for ROS 2 Humble Distributed Nodes
"""

import pytest
import rclpy
from aero_swarm_ros2.sheaf_consensus_node import SheafConsensusNode
from aero_swarm_ros2.ig_etc_trigger_node import IGETCTriggerNode
from aero_swarm_ros2.rta_safety_simplex_node import RTASafetySimplexNode
from aero_swarm_ros2.shata_auction_node import SHATAAuctionNode
from aero_swarm_ros2.rf_jammer_node import RFJammerNode
from aero_swarm_ros2.swarm_world_sim_node import SwarmWorldSimNode


@pytest.fixture(scope="module")
def ros2_context():
    rclpy.init()
    yield
    rclpy.shutdown()


def test_sheaf_consensus_node_init(ros2_context):
    node = SheafConsensusNode(drone_id=0, drone_type=0, total_drones=5)
    assert node.drone_id == 0
    assert node.stalk_dim == 24
    assert node.P.shape == (6, 24)
    node.destroy_node()


def test_ig_etc_trigger_node_init(ros2_context):
    node = IGETCTriggerNode(drone_id=1)
    assert node.drone_id == 1
    d_fr = node.compute_fisher_rao_distance()
    assert d_fr >= 0.0
    node.destroy_node()


def test_rta_safety_simplex_node_init(ros2_context):
    node = RTASafetySimplexNode(drone_id=2, total_drones=5, d_safe=2.5)
    assert node.drone_id == 2
    assert node.d_safe == 2.5
    node.destroy_node()


def test_rf_jammer_node_init(ros2_context):
    node = RFJammerNode(num_jammers=3, jamming_intensity=0.5)
    assert node.num_jammers == 3
    assert node.jamming_intensity == 0.5
    assert len(node.jammers) == 3
    node.destroy_node()


def test_swarm_world_sim_node_init(ros2_context):
    node = SwarmWorldSimNode(num_drones=6, d_safe=2.5)
    assert node.num_drones == 6
    assert node.positions.shape == (6, 3)
    assert node.velocities.shape == (6, 3)
    node.destroy_node()
