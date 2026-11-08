"""
Unit tests for Information Geometry Engine and Fisher-Rao Distance on Gaussian Belief Manifold
"""

import pytest
import numpy as np
from src.core.information_geometry import InformationGeometryEngine


def test_fisher_rao_identity():
    engine = InformationGeometryEngine(state_dim=6)
    mu = np.array([1.0, 2.0, 3.0, 0.5, -0.5, 0.1])
    Sigma = np.eye(6) * 0.2
    
    # Distance to identical belief must be zero
    d_fr = engine.fisher_rao_distance(mu, Sigma, mu, Sigma)
    assert np.isclose(d_fr, 0.0, atol=1e-4)


def test_fisher_rao_positivity_and_symmetry():
    engine = InformationGeometryEngine(state_dim=6)
    mu1 = np.array([1.0, 2.0, 3.0, 0.0, 0.0, 0.0])
    Sigma1 = np.eye(6) * 0.1
    
    mu2 = np.array([4.0, 5.0, 6.0, 1.0, 1.0, 1.0])
    Sigma2 = np.diag([0.2, 0.3, 0.1, 0.2, 0.4, 0.1])
    
    d12 = engine.fisher_rao_distance(mu1, Sigma1, mu2, Sigma2)
    d21 = engine.fisher_rao_distance(mu2, Sigma2, mu1, Sigma1)
    
    assert d12 > 0.0
    assert np.isclose(d12, d21, atol=1e-3)


def test_event_trigger_threshold_adaptation():
    engine = InformationGeometryEngine()
    
    # High energy (E=1.0) -> threshold near delta_min
    thresh_high = engine.delta_min + (engine.delta_max - engine.delta_min) * np.exp(-engine.beta_energy * 1.0)
    
    # Depleted energy (E=0.0) -> threshold near delta_max
    thresh_low = engine.delta_min + (engine.delta_max - engine.delta_min) * np.exp(-engine.beta_energy * 0.0)
    
    assert thresh_high < thresh_low
    assert np.isclose(thresh_low, engine.delta_max)
