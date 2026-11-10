"""
Unit tests for RTA Safety Simplex and Control Barrier Functions
"""

import pytest
import numpy as np
import time
from src.core.safety_cbf import RTASafetySimplex


def test_cbf_safety_evaluation():
    cbf = RTASafetySimplex(d_safe=2.5, alpha_cbf=1.8)
    
    p1 = np.array([0.0, 0.0, 10.0])
    p2 = np.array([3.0, 0.0, 10.0])
    
    # Distance = 3.0 > d_safe = 2.5 => h = 9 - 6.25 = 2.75 > 0
    h_val = cbf.evaluate_inter_drone_cbf(p1, p2)
    assert h_val > 0.0
    assert np.isclose(h_val, 3.0**2 - 2.5**2)


def test_cbf_qp_filter_intervention_on_collision_course():
    cbf = RTASafetySimplex(d_safe=2.5, alpha_cbf=1.8)
    
    p_self = np.array([0.0, 0.0, 10.0])
    p_other = np.array([2.8, 0.0, 10.0]) # close to boundary
    
    # Aggressive velocity directly toward the neighbor
    cmd_dangerous = np.array([5.0, 0.0, 0.0])
    
    safe_cmd, intervened = cbf.filter_control_action(
        drone_idx=0,
        cmd_vel=cmd_dangerous,
        all_positions=np.array([p_self, p_other]),
        obstacles=[]
    )
    
    # Must intervene
    assert intervened is True
    # Safe velocity along x must be reduced or reversed
    assert safe_cmd[0] < cmd_dangerous[0]


def test_cbf_qp_solve_latency_benchmark():
    cbf = RTASafetySimplex(d_safe=2.5, alpha_cbf=1.8)
    
    # 50 drones in dense configuration
    np.random.seed(42)
    positions = np.random.uniform(-20, 20, size=(50, 3))
    cmd = np.array([1.0, 1.0, 0.0])
    
    # Warmup
    for _ in range(10):
        cbf.filter_control_action(drone_idx=0, cmd_vel=cmd, all_positions=positions, obstacles=[])

    latencies = []
    for _ in range(100):
        t0 = time.perf_counter()
        safe_cmd, intervened = cbf.filter_control_action(
            drone_idx=0,
            cmd_vel=cmd,
            all_positions=positions,
            obstacles=[]
        )
        latencies.append((time.perf_counter() - t0) * 1000.0) # ms
        
    p99_lat_ms = np.percentile(latencies, 99)
    # SAE ARP4754B hard real-time requirement: < 1.5 ms
    assert p99_lat_ms < 1.5, f"P99 latency was {p99_lat_ms:.3f} ms, exceeded 1.5 ms limit!"
