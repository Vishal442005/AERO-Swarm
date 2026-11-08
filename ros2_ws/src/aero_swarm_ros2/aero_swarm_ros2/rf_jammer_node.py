#!/usr/bin/env python3
"""
AERO-Swarm: ROS 2 Adversarial RF Jamming Node
Simulates active mobile electronic warfare jammers emitting Gaussian white noise
and directional barrage jamming over wireless mesh channels.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Bool
import numpy as np


class RFJammerNode(Node):
    def __init__(self, num_jammers: int = 2, jamming_intensity: float = 0.4, sweep_pattern: str = 'mobile'):
        super().__init__('rf_jammer_node')
        
        # Declare parameters
        self.declare_parameter('num_jammers', num_jammers)
        self.declare_parameter('jamming_intensity', jamming_intensity)
        self.declare_parameter('sweep_pattern', sweep_pattern)
        
        self.num_jammers = num_jammers
        self.jamming_intensity = jamming_intensity
        self.sweep_pattern = sweep_pattern
        
        # Jammer states: [pos_x, pos_y, pos_z, power, radius]
        self.jammers = []
        for i in range(self.num_jammers):
            p = np.array([
                np.random.uniform(-100.0, 100.0),
                np.random.uniform(-100.0, 100.0),
                np.random.uniform(2.0, 15.0)
            ])
            v = np.random.uniform(-2.5, 2.5, size=3)
            power = 100.0 * (self.jamming_intensity / 0.4)
            radius = 80.0 + 40.0 * self.jamming_intensity
            self.jammers.append({'pos': p, 'vel': v, 'power': power, 'radius': radius})
            
        # Publishers
        self.attenuation_pub = self.create_publisher(
            Float64MultiArray, '/swarm/channel_attenuation', 10
        )
        self.jamming_status_pub = self.create_publisher(
            Bool, '/swarm/jamming_status', 10
        )
        
        # 20 Hz update loop
        self.timer = self.create_timer(0.05, self.update_and_publish)
        self.get_logger().info(f"Initialized RFJammerNode with {self.num_jammers} jammers (Intensity {self.jamming_intensity})")

    def update_and_publish(self):
        # Step mobile jammers
        flat_data = []
        for j in self.jammers:
            if self.sweep_pattern == 'mobile':
                j['pos'] += j['vel'] * 0.05
                # Boundary bounce
                for k in range(2):
                    if abs(j['pos'][k]) > 150.0:
                        j['vel'][k] *= -1.0
            flat_data.extend([j['pos'][0], j['pos'][1], j['pos'][2], j['power'], j['radius']])
            
        msg = Float64MultiArray()
        msg.data = flat_data
        self.attenuation_pub.publish(msg)
        
        status_msg = Bool()
        status_msg.data = self.jamming_intensity > 0.05
        self.jamming_status_pub.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    node = RFJammerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
