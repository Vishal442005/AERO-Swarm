"""
AERO-Swarm: Physical RF Channel and Adversarial Jamming Engine
Simulates Rayleigh fast fading, distance path-loss, multiple mobile/stationary
barrage jammers, Shannon-Hartley channel capacity, and the link integrity factor gamma_{ij}(t).
"""

import numpy as np
from typing import List, Tuple, Dict


class Jammer:
    def __init__(self, position: np.ndarray, power_watts: float = 100.0, 
                 effective_radius: float = 120.0, is_mobile: bool = False,
                 velocity: np.ndarray = None):
        """
        Adversarial Electronic Warfare Jammer.
        """
        self.position = np.array(position, dtype=np.float64)
        self.power = power_watts
        self.radius = effective_radius
        self.is_mobile = is_mobile
        self.velocity = np.zeros(3) if velocity is None else np.array(velocity, dtype=np.float64)

    def step(self, dt: float, bounds: Tuple[float, float, float]):
        """Updates jammer position if mobile."""
        if self.is_mobile:
            self.position += self.velocity * dt
            # Bounce at boundary
            for k in range(3):
                if self.position[k] < -bounds[k] or self.position[k] > bounds[k]:
                    self.velocity[k] *= -1.0


class RFChannelEngine:
    def __init__(self, carrier_freq_mhz: float = 2400.0, 
                 bandwidth_mhz: float = 20.0,
                 tx_power_watts: float = 0.5,
                 path_loss_exponent: float = 3.2,
                 noise_floor_dbm: float = -95.0,
                 sinr_threshold_db: float = 5.0):
        """
        Args:
            carrier_freq_mhz: 2.4 GHz ISM mesh band
            bandwidth_mhz: 20 MHz channel
            tx_power_watts: 500 mW drone SDR transmission power
            path_loss_exponent: 3.2 for cluttered urban canyons
            noise_floor_dbm: -95 dBm thermal noise floor
            sinr_threshold_db: 5 dB minimal decodable SINR
        """
        self.carrier_freq = carrier_freq_mhz * 1e6
        self.bandwidth = bandwidth_mhz * 1e6
        self.tx_power = tx_power_watts
        self.alpha_path = path_loss_exponent
        # Convert noise floor from dBm to Watts
        self.noise_power = 10 ** ((noise_floor_dbm - 30) / 10)
        self.sinr_thresh = 10 ** (sinr_threshold_db / 10)
        self.d0 = 1.0  # Reference distance 1 meter

    def path_loss(self, dist: float) -> float:
        """Computes distance attenuation."""
        d = max(dist, self.d0)
        return (self.d0 / d) ** self.alpha_path

    def compute_link_sinr(self, pos_i: np.ndarray, pos_j: np.ndarray, 
                          jammers: List[Jammer]) -> float:
        """
        Computes instantaneous SINR between drone i and drone j under Rayleigh fading
        and active adversarial RF barrage jammers.
        """
        dist_ij = np.linalg.norm(pos_i - pos_j)
        if dist_ij < 1e-3:
            return 1e6
            
        # Desired signal with Rayleigh fading |h|^2 ~ Exp(1)
        rayleigh_signal = np.random.exponential(scale=1.0)
        signal_power = self.tx_power * rayleigh_signal * self.path_loss(dist_ij)
        
        # Jammer interference
        jamming_interference = 0.0
        for jammer in jammers:
            dist_jam = np.linalg.norm(pos_j - jammer.position)
            if dist_jam <= jammer.radius:
                rayleigh_jam = np.random.exponential(scale=1.0)
                # Attenuation within jamming cone
                jamming_interference += jammer.power * rayleigh_jam * self.path_loss(dist_jam)
                
        sinr = signal_power / (self.noise_power + jamming_interference)
        return float(sinr)

    def compute_link_integrity(self, sinr: float) -> float:
        """
        Computes smooth link integrity factor gamma_{ij} in [0, 1]
        based on Shannon-Hartley capacity relative to decodable threshold.
        """
        capacity = self.bandwidth * np.log2(1.0 + sinr)
        threshold_capacity = self.bandwidth * np.log2(1.0 + self.sinr_thresh)
        
        # Sigmoid transition centered at threshold capacity
        diff_ratio = (capacity - threshold_capacity) / (threshold_capacity + 1e-6)
        gamma = 1.0 / (1.0 + np.exp(-3.0 * diff_ratio))
        return float(np.clip(gamma, 0.0, 1.0))

    def evaluate_mesh_links(self, positions: np.ndarray, 
                            comm_radius: float, 
                            jammers: List[Jammer]
                            ) -> Tuple[List[Tuple[int, int]], Dict[Tuple[int, int], float]]:
        """
        Computes all active pairwise links within communication radius and evaluates
        their individual link integrity factors under active jamming.
        
        Returns:
            edges: List of (u, v) pairs within range
            integrities: Dict mapping (u, v) -> gamma_uv in [0, 1]
        """
        num_drones = len(positions)
        edges = []
        integrities = {}
        
        for i in range(num_drones):
            for j in range(i + 1, num_drones):
                dist = np.linalg.norm(positions[i] - positions[j])
                if dist <= comm_radius:
                    # Symmetric channel evaluation
                    sinr_ij = self.compute_link_sinr(positions[i], positions[j], jammers)
                    sinr_ji = self.compute_link_sinr(positions[j], positions[i], jammers)
                    sinr_eff = min(sinr_ij, sinr_ji)
                    
                    gamma = self.compute_link_integrity(sinr_eff)
                    edges.append((i, j))
                    edges.append((j, i))
                    integrities[(i, j)] = gamma
                    integrities[(j, i)] = gamma
                    
        return edges, integrities
