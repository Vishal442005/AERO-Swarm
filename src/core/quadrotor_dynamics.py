"""
AERO-Swarm: Heterogeneous Quadrotor Dynamics on SE(3)
Simulates translational, rotational, aerodynamic drag, energy depletion,
wind turbulence, and GPS-denied visual odometry drift across 3 drone classes.
"""

import numpy as np
from typing import Dict, Any, Tuple


class DroneSpecs:
    PROPERTIES = {
        0: { # LEADER
            'mass': 1.6,             # kg
            'thrust_max': 32.0,      # N
            'speed_max': 12.0,       # m/s
            'battery_joules': 180e3, # 180 kJ (approx 20 mins flight)
            'compute_power': 18.5,   # Watts (Edge GPU SLAM)
            'hover_power': 140.0,    # Watts
            'drag_coeff': 0.18,
            'vio_drift_rate': 0.08   # m/s drift rate in GPS-denied
        },
        1: { # SCOUT
            'mass': 0.65,            # kg
            'thrust_max': 18.0,      # N
            'speed_max': 20.0,       # m/s (high agility)
            'battery_joules': 75e3,  # 75 kJ (approx 12 mins flight)
            'compute_power': 2.5,    # Watts (Microcontroller/IMU)
            'hover_power': 65.0,     # Watts
            'drag_coeff': 0.08,
            'vio_drift_rate': 0.25   # Higher drift rate (lightweight camera)
        },
        2: { # RELAY
            'mass': 1.1,             # kg
            'thrust_max': 24.0,      # N
            'speed_max': 14.0,       # m/s
            'battery_joules': 120e3, # 120 kJ (approx 16 mins flight)
            'compute_power': 8.0,    # Watts (SDR transceivers)
            'hover_power': 95.0,     # Watts
            'drag_coeff': 0.14,
            'vio_drift_rate': 0.12
        }
    }


class HeterogeneousDrone:
    def __init__(self, drone_id: int, drone_type: int, initial_pos: np.ndarray):
        self.id = drone_id
        self.type = drone_type
        self.specs = DroneSpecs.PROPERTIES[drone_type]
        
        # Physical True States (World Frame)
        self.pos = np.array(initial_pos, dtype=np.float64)
        self.vel = np.zeros(3, dtype=np.float64)
        self.yaw = 0.0 # Radians
        self.omega_z = 0.0
        
        # Onboard Estimated Belief State (GPS-Denied VIO drift model)
        self.est_pos = np.copy(self.pos)
        self.est_vel = np.copy(self.vel)
        self.est_cov = np.eye(6) * 0.01  # Covariance on (pos, vel)
        
        # Energy reserve
        self.energy = self.specs['battery_joules']
        self.is_alive = True
        
        # Inter-agent communication tracking
        self.last_tx_belief_mu = np.concatenate([self.est_pos, self.est_vel])
        self.last_tx_belief_Sigma = np.copy(self.est_cov)
        self.total_tx_events = 0
        self.total_tx_bytes = 0

    def step_physics(self, cmd_vel: np.ndarray, cmd_yaw_rate: float, 
                     dt: float, wind_turbulence: np.ndarray,
                     mutual_observation_active: bool = False):
        """
        Integrates continuous equations of motion over timestep dt.
        """
        if not self.is_alive or self.energy <= 0.0:
            self.is_alive = False
            self.vel = np.zeros(3)
            return
            
        # Velocity control with actuator limits and parasitic drag
        v_target = np.clip(cmd_vel, -self.specs['speed_max'], self.specs['speed_max'])
        accel = (v_target - self.vel) / 0.15  # Actuator time constant 150 ms
        
        # Aerodynamic drag and wind disturbance
        drag = -self.specs['drag_coeff'] * self.vel * np.linalg.norm(self.vel)
        total_accel = accel + (drag / self.specs['mass']) + wind_turbulence
        
        # Update true position and velocity
        self.vel += total_accel * dt
        # Clamp velocity
        speed = np.linalg.norm(self.vel)
        if speed > self.specs['speed_max']:
            self.vel = (self.vel / speed) * self.specs['speed_max']
            
        self.pos += self.vel * dt
        # Ensure above ground
        self.pos[2] = max(1.0, self.pos[2])
        
        # Yaw dynamics
        self.yaw = (self.yaw + cmd_yaw_rate * dt) % (2 * np.pi)
        
        # Update GPS-denied VIO estimation drift
        # Mutual observation actively arrests drift by 65% (Active-FoV mechanism)
        drift_factor = 0.35 if mutual_observation_active else 1.0
        drift_step = np.random.normal(0, self.specs['vio_drift_rate'] * drift_factor * np.sqrt(dt), size=3)
        self.est_pos = self.pos + drift_step
        self.est_vel = self.vel + np.random.normal(0, 0.05 * np.sqrt(dt), size=3)
        
        # Covariance inflation
        self.est_cov[0:3, 0:3] += np.eye(3) * (self.specs['vio_drift_rate'] * drift_factor * dt)
        if mutual_observation_active:
            # Observability update contracts estimation covariance
            self.est_cov *= 0.95
            
        # Deplete battery energy
        power_motion = self.specs['hover_power'] + 0.5 * self.specs['mass'] * (speed ** 2)
        power_compute = self.specs['compute_power']
        total_power = power_motion + power_compute
        self.energy -= total_power * dt
        if self.energy <= 0.0:
            self.energy = 0.0
            self.is_alive = False

    def log_transmission(self, packet_bytes: int = 64):
        """Logs an event-triggered transmission."""
        self.total_tx_events += 1
        self.total_tx_bytes += packet_bytes
        # RF amplifier power surge: 1.5 Watts for 10 ms
        self.energy -= 1.5 * 0.01
        self.last_tx_belief_mu = np.concatenate([self.est_pos, self.est_vel])
        self.last_tx_belief_Sigma = np.copy(self.est_cov)

    @property
    def energy_ratio(self) -> float:
        return float(self.energy / self.specs['battery_joules'])

    @property
    def belief_state(self) -> Tuple[np.ndarray, np.ndarray]:
        mu = np.concatenate([self.est_pos, self.est_vel])
        return mu, self.est_cov
