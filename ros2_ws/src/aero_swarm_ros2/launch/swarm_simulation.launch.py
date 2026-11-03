from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    nodes = []
    
    # Instantiate 3 heterogeneous drones (0: Leader, 1: Scout, 2: Relay)
    fleet = [
        {'id': 0, 'type': 0}, # Leader
        {'id': 1, 'type': 1}, # Scout
        {'id': 2, 'type': 2}, # Relay
    ]
    
    for drone in fleet:
        d_id = drone['id']
        d_type = drone['type']
        
        # 1. Sheaf Consensus Node
        nodes.append(Node(
            package='aero_swarm_ros2',
            executable='sheaf_consensus_node',
            name=f'sheaf_consensus_drone_{d_id}',
            parameters=[{'drone_id': d_id, 'drone_type': d_type}],
            output='screen'
        ))
        
        # 2. Information-Geometric Trigger Node
        nodes.append(Node(
            package='aero_swarm_ros2',
            executable='ig_etc_trigger_node',
            name=f'ig_etc_trigger_drone_{d_id}',
            parameters=[{'drone_id': d_id}],
            output='screen'
        ))
        
        # 3. RTA Safety Simplex Node
        nodes.append(Node(
            package='aero_swarm_ros2',
            executable='rta_safety_simplex_node',
            name=f'rta_safety_simplex_drone_{d_id}',
            parameters=[{'drone_id': d_id}],
            output='screen'
        ))
        
        # 4. SHATA Auction Node
        nodes.append(Node(
            package='aero_swarm_ros2',
            executable='shata_auction_node',
            name=f'shata_auction_drone_{d_id}',
            parameters=[{'drone_id': d_id, 'drone_type': d_type}],
            output='screen'
        ))
        
    return LaunchDescription(nodes)
