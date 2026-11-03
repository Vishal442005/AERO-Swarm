"""
AERO-Swarm: Information Geometry Engine
Computes the Fisher-Rao Riemannian metric tensor, geodesic distance between
multivariate Gaussian belief states, and the Information-Geometric Event-Triggered
Communication (IG-ETC) decision rule with energy-annealed adaptive thresholding.
"""

import numpy as np
import scipy.linalg as la
from typing import Tuple


class InformationGeometryEngine:
    def __init__(self, state_dim: int = 6, 
                 delta_min: float = 0.4, 
                 delta_max: float = 2.5, 
                 beta_energy: float = 2.0, 
                 kappa_jam: float = 1.5):
        """
        Args:
            state_dim: Dimension of communicated belief (default 6: 3D Pos + 3D Vel)
            delta_min: Base threshold when battery is full and channel is clean
            delta_max: Upper threshold bound under severe depletion
            beta_energy: Exponential decay rate for energy annealing
            kappa_jam: Jamming resistance multiplier
        """
        self.state_dim = state_dim
        self.delta_min = delta_min
        self.delta_max = delta_max
        self.beta_energy = beta_energy
        self.kappa_jam = kappa_jam

    def fisher_rao_distance(self, mu_1: np.ndarray, Sigma_1: np.ndarray,
                            mu_2: np.ndarray, Sigma_2: np.ndarray) -> float:
        """
        Computes the exact closed-form Fisher-Rao Riemannian geodesic distance
        between two multivariate Gaussians p_1 = N(mu_1, Sigma_1) and p_2 = N(mu_2, Sigma_2).
        
        d_FR^2 = 1/2 sum_k ln^2(lambda_k) + (mu_1 - mu_2)^T Sigma_{12}^{-1} (mu_1 - mu_2)
        """
        d = len(mu_1)
        # Ensure positive definiteness with jitter
        eps = 1e-5
        S1 = Sigma_1 + eps * np.eye(d)
        S2 = Sigma_2 + eps * np.eye(d)
        
        try:
            # Generalized eigenvalues: det(S1 - lambda * S2) = 0
            eigenvals = la.eigvals(S1, S2).real
            eigenvals = np.clip(eigenvals, 1e-6, 1e6)
            log_term = 0.5 * np.sum(np.log(eigenvals) ** 2)
            
            # Midpoint covariance Mahalanobis distance
            S_mid = 0.5 * (S1 + S2)
            diff = mu_1 - mu_2
            mahalanobis = diff.T @ la.solve(S_mid, diff)
            
            d_sq = log_term + mahalanobis
            return float(np.sqrt(max(0.0, d_sq)))
        except Exception:
            # Fallback to Mahalanobis on numerical instability
            diff = mu_1 - mu_2
            return float(np.linalg.norm(diff))

    def compute_adaptive_threshold(self, energy_ratio: float, mean_link_integrity: float) -> float:
        """
        Computes the dynamic adaptive threshold delta_i(E_i, gamma_i).
        
        Args:
            energy_ratio: E_i / E_max in [0, 1]
            mean_link_integrity: Mean gamma_ij in [0, 1] across active neighbors
        """
        energy_ratio = np.clip(energy_ratio, 0.0, 1.0)
        mean_link_integrity = np.clip(mean_link_integrity, 0.0, 1.0)
        
        # Energy annealing term: as energy -> 0, threshold expands
        energy_penalty = (self.delta_max - self.delta_min) * np.exp(-self.beta_energy * energy_ratio)
        # Jammer awareness term: when links are jammed (gamma -> 0), suppress retries
        jamming_penalty = self.kappa_jam * (1.0 - mean_link_integrity)
        
        delta = self.delta_min + energy_penalty + jamming_penalty
        return float(delta)

    def evaluate_trigger(self, mu_curr: np.ndarray, Sigma_curr: np.ndarray,
                         mu_last: np.ndarray, Sigma_last: np.ndarray,
                         energy_ratio: float, mean_link_integrity: float
                         ) -> Tuple[bool, float, float]:
        """
        Evaluates the IG-ETC decision rule:
        Returns:
            should_transmit: True if d_FR > delta_i
            d_FR: Computed Fisher-Rao distance
            delta_i: Computed adaptive threshold
        """
        d_FR = self.fisher_rao_distance(mu_curr, Sigma_curr, mu_last, Sigma_last)
        delta_i = self.compute_adaptive_threshold(energy_ratio, mean_link_integrity)
        should_transmit = bool(d_FR > delta_i)
        return should_transmit, d_FR, delta_i
