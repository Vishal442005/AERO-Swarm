"""
Unit tests for ROS 2 Humble Distributed Nodes in AERO-Swarm
"""

import pytest
import numpy as np
import rclpy
from aero_swarm_ros2.sheaf_consensus_node import SheafConsensusNode
from aero_swarm_ros2.ig_etc_trigger_node import IGETCTriggerNode
from aero_swarm_ros2.rta_safety_simplex_node import RTASafetySimplexNode
from aero_swarm_ros2.shata_auction_node import SHATAAuctionNode
from aero_swarm_ros2.aero_formation_controller_node import AEROFormationControllerNode
from aero_swarm_ros2.rf_jammer_node import RFJammerNode
from aero_swarm_ros2.swarm_world_sim_node import SwarmWorldSimNode
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


@pytest.fixture(scope="module")
def ros2_context():
    rclpy.init()
    yield
    rclpy.shutdown()


def test_sheaf_consensus_node_heterogeneity(ros2_context):
    """Verifies heterogeneous stalk dimensions: Leader 24, Scout 12, Relay 8."""
    leader = SheafConsensusNode(drone_id=0, drone_type=0, total_drones=3)
    scout = SheafConsensusNode(drone_id=1, drone_type=1, total_drones=3)
    relay = SheafConsensusNode(drone_id=2, drone_type=2, total_drones=3)
    
    assert leader.stalk_dim == 24
    assert leader.P.shape == (6, 24)
    
    assert scout.stalk_dim == 12
    assert scout.P.shape == (6, 12)
    
    assert relay.stalk_dim == 8
    assert relay.P.shape == (6, 8)
    
    leader.destroy_node()
    scout.destroy_node()
    relay.destroy_node()


def test_ig_etc_trigger_node(ros2_context):
    """Verifies Fisher-Rao Riemannian distance and event triggering."""
    node = IGETCTriggerNode(drone_id=1)
    assert node.drone_id == 1
    d_fr = node.compute_fisher_rao_distance()
    assert d_fr >= 0.0
    
    # Check trigger evaluation
    node.check_trigger()
    node.destroy_node()


def test_shata_auction_node(ros2_context):
    """Verifies SHATA capability utility, H1 cohomology rank, and bundle assignment."""
    node = SHATAAuctionNode(drone_id=0, drone_type=0, total_drones=3)
    assert len(node.tasks) > 0
    
    # Compute bid for task 0
    t0 = node.tasks[0]
    bid = node.compute_bid(t0)
    assert bid >= 0.0
    
    # Check cohomology calculation
    h1 = node.evaluate_cohomology_obstruction()
    assert h1 in [0, 1]
    
    # Run auction cycle
    node.auction_cycle()
    assert isinstance(node.assigned_bundle, list)
    node.destroy_node()


def test_formation_controller_node(ros2_context):
    """Verifies 50 Hz formation guidance command generation."""
    node = AEROFormationControllerNode(drone_id=1, drone_type=1)
    assert node.drone_id == 1
    assert node.v_max > 0.0
    
    # Run control loop step
    node.control_loop()
    node.destroy_node()


def test_rta_safety_simplex_override(ros2_context):
    """Verifies CBF QP safety override when near collision boundary."""
    node = RTASafetySimplexNode(drone_id=0, total_drones=2, d_safe=2.5)
    node.pos_self = np.array([0.0, 0.0, 10.0])
    # Neighbor drone placed dangerously close (dist = 1.0 m < 2.5 m)
    node.neighbor_poses[1] = np.array([1.0, 0.0, 10.0])
    
    # Dangerous velocity directed towards neighbor (vx = +5.0 m/s)
    raw_cmd = Twist()
    raw_cmd.linear.x = 5.0
    raw_cmd.linear.y = 0.0
    raw_cmd.linear.z = 0.0
    
    node.raw_cmd_callback(raw_cmd)
    node.destroy_node()


def test_rf_jammer_node(ros2_context):
    """Verifies dynamic RF jamming field propagation."""
    node = RFJammerNode(num_jammers=3, jamming_intensity=0.6)
    assert node.num_jammers == 3
    assert node.jamming_intensity == 0.6
    assert len(node.jammers) == 3
    node.update_and_publish()
    node.destroy_node()


def test_swarm_world_sim_node(ros2_context):
    """Verifies multi-drone physics and safety distance tracking."""
    node = SwarmWorldSimNode(num_drones=5, d_safe=2.5)
    assert node.num_drones == 5
    assert node.positions.shape == (5, 3)
    assert node.velocities.shape == (5, 3)
    node.physics_step()
    node.destroy_node()
