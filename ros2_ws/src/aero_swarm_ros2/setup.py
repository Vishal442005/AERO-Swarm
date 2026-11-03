import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'aero_swarm_ros2'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name if os.path.exists('resource/' + package_name) else 'package.xml']),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='AERO-Swarm Research Team',
    maintainer_email='jarvis@autonomous-swarms.org',
    description='AERO-Swarm ROS 2 Package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sheaf_consensus_node = aero_swarm_ros2.sheaf_consensus_node:main',
            'ig_etc_trigger_node = aero_swarm_ros2.ig_etc_trigger_node:main',
            'rta_safety_simplex_node = aero_swarm_ros2.rta_safety_simplex_node:main',
            'shata_auction_node = aero_swarm_ros2.shata_auction_node:main',
        ],
    },
)
