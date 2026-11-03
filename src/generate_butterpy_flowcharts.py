"""
generate_butterpy_flowcharts.py
Uses the butterpy Python extension to generate simple, publication-grade flowcharts
with standard shapes (rectangles, diamonds, capsules), crisp black arrows, clear text,
and domain icons.
"""

import os
import sys

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.butterpy import ButterFlowchart

def build_aero_flowchart(output_path):
    fc = ButterFlowchart(title="AERO-Swarm Coordination & Resilience Flowchart (Generated with butterpy)", width=16, height=10)

    # Top Row: Ingestion & Information-Geometric Gating
    fc.add_node("start", "Swarm Initialization", shape_type="capsule", x=2.5, y=8.2, width=3.4, height=1.1,
                icon="drone", color="#EFF6FF", border_color="#2563EB", subtitle="Heterogeneous Fleet (Scouts, Leaders, Relays)")

    fc.add_node("belief", "Onboard Belief Dynamics", shape_type="box", x=7.0, y=8.2, width=3.6, height=1.1,
                icon="sensor", color="#F0FDF4", border_color="#16A34A", subtitle="p_i(t) ~ N(μ_i, Σ_i) ∈ P_+^6 (LiDAR/VIO Fusion)")

    fc.add_node("ig_etc", "Fisher-Rao Event Trigger?", shape_type="diamond", x=12.2, y=8.2, width=3.4, height=1.3,
                icon="decision", color="#FEF3C7", border_color="#D97706", subtitle="d_FR^2(p_i, p_{last}) ≥ δ_i(t)?")

    fc.add_node("silent", "Radio Silence Mode", shape_type="box", x=14.6, y=5.5, width=2.5, height=1.0,
                color="#F1F5F9", border_color="#64748B", subtitle="79.7% Bandwidth Saved")

    # Middle Row: Algebraic Sheaf Topology & Jamming Detection
    fc.add_node("sheaf", "Cellular Sheaf Channel Mapping", shape_type="box", x=11.2, y=5.5, width=3.6, height=1.1,
                icon="sheaf", color="#FAF5FF", border_color="#7C3AED", subtitle="Project F_v → F_e via ρ_{v⊴e}(t) & Build L_F")

    fc.add_node("curvature", "Bochner SCVI Jamming Check", shape_type="diamond", x=6.8, y=5.5, width=3.4, height=1.3,
                icon="decision", color="#FEF3C7", border_color="#D97706", subtitle="κ_v(t) = λ_min(Ric_F) < 0?")

    fc.add_node("reroute", "Curvature Jamming Reroute", shape_type="box", x=6.8, y=3.2, width=3.4, height=1.0,
                icon="jammer", color="#FEF2F2", border_color="#DC2626", subtitle="Steer Relays Away from Jamming Cones")

    # Bottom-Left & Actuation: Auction & Safety Simplex
    fc.add_node("auction", "SHATA Task Allocation", shape_type="box", x=2.5, y=5.5, width=3.4, height=1.1,
                icon="target", color="#ECFDF5", border_color="#059669", subtitle="Bundle Auctions & Cochain Consensus")

    fc.add_node("simplex", "Hardware RTA Simplex Check", shape_type="diamond", x=2.5, y=3.2, width=3.4, height=1.3,
                icon="shield", color="#FEF3C7", border_color="#D97706", subtitle="CBF Invariance h_safe(x) ≥ 0?")

    fc.add_node("fallback", "Certified Fallback Controller", shape_type="box", x=2.5, y=1.2, width=3.0, height=0.9,
                color="#FEF2F2", border_color="#DC2626", subtitle="Sub-1.2 ms QP Emergency Avoidance")

    fc.add_node("flight", "PX4 Trajectory Actuation", shape_type="box", x=7.8, y=1.2, width=3.6, height=1.1,
                icon="drone", color="#EFF6FF", border_color="#2563EB", subtitle="50 Hz SE(3) Control & Resilient Flocking")

    fc.add_node("end", "Mission Goal Completed", shape_type="capsule", x=12.8, y=1.2, width=3.4, height=1.1,
                icon="target", color="#F0FDF4", border_color="#16A34A", subtitle="0 Safety Violations & >91.3% TCR")

    # Connecting Black Arrows
    fc.add_arrow("start", "belief", label="Telemetric Stream", label_offset=(0, 0.22))
    fc.add_arrow("belief", "ig_etc", label="Belief Divergence", label_offset=(0, 0.22))

    # Event trigger branches
    fc.add_arrow("ig_etc", "silent", label="NO (Radio Silence)", label_offset=(0, 0.2),
                 waypoints=[(12.2, 7.0), (14.6, 7.0)])
    fc.add_arrow("silent", "belief", label="Conserve RF Spectrum", label_offset=(0, -0.2),
                 waypoints=[(14.6, 9.0), (7.0, 9.0)])
    fc.add_arrow("ig_etc", "sheaf", label="YES (Broadcast)", label_offset=(0.2, 0))

    # Sheaf & Curvature
    fc.add_arrow("sheaf", "curvature", label="Sheaf Laplacian L_F", label_offset=(0, 0.22))
    fc.add_arrow("curvature", "reroute", label="YES (Bottleneck)", label_offset=(0.2, 0))
    fc.add_arrow("curvature", "auction", label="NO (Clear)", label_offset=(0, 0.22))
    fc.add_arrow("reroute", "auction", label="Rerouted Cochains", label_offset=(0, -0.2),
                 waypoints=[(5.0, 3.2), (2.5, 4.5)])

    # Task allocation & Safety Simplex
    fc.add_arrow("auction", "simplex", label="Policy Trajectory", label_offset=(0.2, 0))
    fc.add_arrow("simplex", "fallback", label="NO (Violation)", label_offset=(0.2, 0))
    fc.add_arrow("simplex", "flight", label="YES (Nominal Safe)", label_offset=(0, 0.2),
                 waypoints=[(4.8, 3.2), (4.8, 1.2)])
    fc.add_arrow("fallback", "flight", label="Certified Action", label_offset=(0, 0.22))
    fc.add_arrow("flight", "end", label="Resilient Swarm Formation", label_offset=(0, 0.22))

    fc.render(output_path)

if __name__ == "__main__":
    out1 = "/media/jarvis/01DB55B559EC9500/Robotics Swarm/results/fig_butterpy_flowchart.png"
    out2 = "/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_ieee_(T-Cyb)/figures/fig_butterpy_flowchart.png"
    out3 = "/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_elseiver_(SWEVO)_RAS/figures/fig_butterpy_flowchart.png"
    out_art = "/home/jarvis/.gemini/antigravity/brain/fafe8fae-1dc3-4e8d-9de8-adc10005550e/fig_butterpy_flowchart.png"

    build_aero_flowchart(out1)
    build_aero_flowchart(out2)
    build_aero_flowchart(out3)
    build_aero_flowchart(out_art)
    print("All butterpy flowcharts generated successfully!")
