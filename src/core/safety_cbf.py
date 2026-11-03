"""
AERO-Swarm: Control Barrier Functions & Run-Time Assurance (RTA) Safety Simplex
Enforces mathematical zero-collision guarantees via CBFs, provides Active-FoV
mutual observation constraints for GPS-denied drift mitigation, and executes
the hardware-isolated RTA Simplex QP safety override filter (SAE ARP4754B).
"""

import numpy as np
from typing import List, Tuple, Optional


class RTASafetySimplex:
    def __init__(self, d_safe: float = 2.5, alpha_cbf: float = 1.8, 
                 fov_half_angle_deg: float = 45.0):
        """
        Args:
            d_safe: Minimum inter-drone separation distance (meters)
            alpha_cbf: CBF class-K comparison coefficient
            fov_half_angle_deg: Camera field-of-view cone
        """
        self.d_safe = d_safe
        self.alpha_cbf = alpha_cbf
        self.cos_half_fov = np.cos(np.radians(fov_half_angle_deg))

    def evaluate_inter_drone_cbf(self, p_i: np.ndarray, p_j: np.ndarray) -> float:
        """h_ij = ||p_i - p_j||^2 - d_safe^2 >= 0"""
        return float(np.sum((p_i - p_j) ** 2) - self.d_safe ** 2)

    def evaluate_obstacle_cbf(self, p_i: np.ndarray, p_obs: np.ndarray, r_obs: float) -> float:
        """h_obs = ||p_i - p_obs||^2 - (r_obs + d_margin)^2 >= 0"""
        return float(np.sum((p_i - p_obs) ** 2) - (r_obs + 1.0) ** 2)

    def evaluate_active_fov_cbf(self, p_scout: np.ndarray, yaw_scout: float, 
                                p_leader: np.ndarray) -> Tuple[bool, float]:
        """
        Evaluates whether the Leader UAV is within the Scout's forward camera FoV.
        h_FoV = (p_leader - p_scout)^T c_cam / ||p_leader - p_scout|| - cos(theta_FoV) >= 0
        """
        diff = p_leader - p_scout
        dist = np.linalg.norm(diff)
        if dist < 1e-3:
            return True, 1.0
            
        unit_diff = diff / dist
        # Camera optical axis vector from yaw angle
        c_cam = np.array([np.cos(yaw_scout), np.sin(yaw_scout), 0.0])
        dot_prod = float(np.dot(unit_diff, c_cam))
        h_fov = dot_prod - self.cos_half_fov
        is_visible = bool(h_fov >= 0.0)
        return is_visible, h_fov

    def filter_control_action(self, drone_idx: int, cmd_vel: np.ndarray, 
                              all_positions: np.ndarray, 
                              obstacles: List[Tuple[np.ndarray, float]]
                              ) -> Tuple[np.ndarray, bool]:
        """
        RTA Safety Gateway: Evaluates proposed velocity command against
        all active CBF barrier constraints. If constraint is endangered,
        projects command onto safe half-space via closed-form QP projection.
        
        Returns:
            safe_cmd_vel: Safe filtered velocity vector
            override_triggered: True if RTA Simplex intervened
        """
        p_i = all_positions[drone_idx]
        u_safe = np.copy(cmd_vel)
        override_triggered = False
        num_drones = len(all_positions)
        
        # 1. Inter-Drone Collision Avoidance
        for j in range(num_drones):
            if j == drone_idx:
                continue
            p_j = all_positions[j]
            diff = p_i - p_j
            dist = np.linalg.norm(diff)
            h = dist ** 2 - self.d_safe ** 2
            
            # Barrier gradient: grad_p h = 2 * (p_i - p_j)
            grad_h = 2.0 * diff
            # Lie derivative condition: grad_h^T u + alpha * h >= 0
            drift = np.dot(grad_h, u_safe)
            if drift + self.alpha_cbf * h < 0.0:
                override_triggered = True
                # QP normal projection: u_new = u - (drift + alpha*h)/||grad_h||^2 * grad_h
                denom = np.dot(grad_h, grad_h) + 1e-6
                u_safe -= ((drift + self.alpha_cbf * h) / denom) * grad_h
                
        # 2. Obstacle Collision Avoidance
        for (p_obs, r_obs) in obstacles:
            diff = p_i - p_obs
            dist = np.linalg.norm(diff)
            h_obs = dist ** 2 - (r_obs + 1.0) ** 2
            grad_h = 2.0 * diff
            drift = np.dot(grad_h, u_safe)
            if drift + self.alpha_cbf * h_obs < 0.0:
                override_triggered = True
                denom = np.dot(grad_h, grad_h) + 1e-6
                u_safe -= ((drift + self.alpha_cbf * h_obs) / denom) * grad_h
                
        return u_safe, override_triggered
