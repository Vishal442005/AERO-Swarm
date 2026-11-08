from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    nodes = []
    
    # Instantiate heterogeneous fleet (0: Leader, 1: Scout, 2: Relay)
    fleet = [
        {'id': 0, 'type': 0}, # Leader (Stalk 24)
        {'id': 1, 'type': 1}, # Scout  (Stalk 12)
        {'id': 2, 'type': 2}, # Relay  (Stalk 8)
    ]
    num_drones = len(fleet)
    
    # 1. Swarm World Physics Simulation Node
    nodes.append(Node(
        package='aero_swarm_ros2',
        executable='swarm_world_sim_node',
        name='swarm_world_sim',
        parameters=[{'num_drones': num_drones, 'd_safe': 2.5}],
        output='screen'
    ))
    
    # 2. RF Electronic Warfare Jammer Node
    nodes.append(Node(
        package='aero_swarm_ros2',
        executable='rf_jammer_node',
        name='rf_jammer_node',
        parameters=[{'num_jammers': 2, 'jamming_intensity': 0.5}],
        output='screen'
    ))
    
    # 3. Instantiate Per-Drone Nodes
    for drone in fleet:
        d_id = drone['id']
        d_type = drone['type']
        
        # Sheaf Coordinator (Consensus)
        nodes.append(Node(
            package='aero_swarm_ros2',
            executable='sheaf_consensus_node',
            name=f'sheaf_consensus_drone_{d_id}',
            parameters=[{'drone_id': d_id, 'drone_type': d_type, 'total_drones': num_drones}],
            output='screen'
        ))
        
        # Formation Controller (50 Hz Guidance)
        nodes.append(Node(
            package='aero_swarm_ros2',
            executable='aero_formation_controller',
            name=f'aero_formation_controller_drone_{d_id}',
            parameters=[{'drone_id': d_id, 'drone_type': d_type}],
            output='screen'
        ))
        
        # Information-Geometric Trigger (Fisher-Rao ETC)
        nodes.append(Node(
            package='aero_swarm_ros2',
            executable='ig_etc_trigger_node',
            name=f'ig_etc_trigger_drone_{d_id}',
            parameters=[{'drone_id': d_id}],
            output='screen'
        ))
        
        # RTA Safety Simplex (CBF QP Override)
        nodes.append(Node(
            package='aero_swarm_ros2',
            executable='rta_safety_simplex_node',
            name=f'rta_safety_simplex_drone_{d_id}',
            parameters=[{'drone_id': d_id, 'total_drones': num_drones, 'd_safe': 2.5}],
            output='screen'
        ))
        
        # SHATA Task Allocator (Capability Auction)
        nodes.append(Node(
            package='aero_swarm_ros2',
            executable='shata_auction_node',
            name=f'shata_auction_drone_{d_id}',
            parameters=[{'drone_id': d_id, 'drone_type': d_type, 'total_drones': num_drones}],
            output='screen'
        ))
        
    return LaunchDescription(nodes)
