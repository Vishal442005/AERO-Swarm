"""
generate_all_3_butterpy_flowcharts.py
Generates the 3 distinct, ultra-simple, publication-grade flowcharts using butterpy:
1. Sheaf-Theoretic Distributed Swarm Coordination
2. Information-Geometric Event-Triggered Communication (IG-ETC)
3. Decentralized SHATA Task Allocation & RTA Simplex Safety

Design Constraints:
- Pure white box fills (strictly NO colors inside boxes)
- Solid black outlines, solid black arrows, solid black text
- Minimalist black vector icons
- Standard shapes: Capsule (Terminal), Rectangle (Process), Diamond (Decision)
- Everything as simple as possible
"""

import os
import sys
import shutil

# Ensure src is on path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.butterpy import ButterFlowchart

def distribute_file(primary_path, all_paths):
    for p in all_paths:
        if p != primary_path:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            shutil.copyfile(primary_path, p)
            print(f"Copied {primary_path} -> {p}")

def make_flowchart1(out_paths):
    """Flowchart 1: Sheaf-Theoretic Distributed Swarm Coordination Pipeline"""
    fc = ButterFlowchart(
        title="Flowchart 1: Sheaf-Theoretic Distributed Swarm Coordination",
        width=8.0, height=11.2
    )

    # 1. Start Capsule
    fc.add_node("start", "Swarm Initialization", shape_type="capsule",
                x=4.0, y=10.0, width=4.6, height=0.75, icon="drone",
                subtitle="N = 200 Heterogeneous Agents (Scouts, Leaders, Relays)")

    # 2. State Estimation Box
    fc.add_node("belief", "Local Belief State Estimation", shape_type="box",
                x=4.0, y=8.7, width=4.6, height=0.75, icon="sensor",
                subtitle="VIO / LiDAR Fusion: p_i(t) ~ N(μ_i, Σ_i)")

    # 3. Sheaf Laplacian Box
    fc.add_node("sheaf", "Cellular Sheaf Construction", shape_type="box",
                x=4.0, y=7.4, width=4.6, height=0.75, icon="sheaf",
                subtitle="Restriction Maps ρ_{u⊴e} & Sheaf Laplacian L_F")

    # 4. Curvature Check Diamond
    fc.add_node("curv_dec", "Forman-Ricci Curvature\nκ(e) < 0 (Jamming)?", shape_type="diamond",
                x=4.0, y=5.8, width=4.2, height=1.1, icon="decision")

    # 5a. Reweighting Box (Left branch)
    fc.add_node("reweight", "Topological Reweighting", shape_type="box",
                x=1.8, y=4.4, width=3.0, height=0.75, icon="jammer",
                subtitle="Attenuate Jammed Edges")

    # 5b. Nominal Box (Right branch)
    fc.add_node("nominal", "Nominal Diffusion", shape_type="box",
                x=6.2, y=4.4, width=3.0, height=0.75, icon="sheaf",
                subtitle="Standard Harmonic Flow")

    # 6. Consensus Box
    fc.add_node("consensus", "Distributed Cochain Consensus", shape_type="box",
                x=4.0, y=3.0, width=4.6, height=0.75, icon="shield",
                subtitle="Solve: x_k+1 = x_k - α L_F x_k")

    # 7. Actuation Box
    fc.add_node("actuation", "Decentralized Motor Actuation", shape_type="box",
                x=4.0, y=1.8, width=4.6, height=0.75, icon="drone",
                subtitle="50 Hz SE(3) Tracking & Formation Control")

    # 8. End Capsule
    fc.add_node("end", "Mission Goal Convergence", shape_type="capsule",
                x=4.0, y=0.7, width=4.6, height=0.75, icon="target",
                subtitle="Resilient Coordination with Zero Violations")

    # Connect with crisp black arrows
    fc.add_arrow("start", "belief")
    fc.add_arrow("belief", "sheaf")
    fc.add_arrow("sheaf", "curv_dec")

    # Branches from decision
    fc.add_arrow("curv_dec", "reweight", label="Yes", label_offset=(-0.15, 0.1),
                 from_port="left", to_port="top", waypoints=[(1.8, 5.8)])
    fc.add_arrow("curv_dec", "nominal", label="No", label_offset=(0.15, 0.1),
                 from_port="right", to_port="top", waypoints=[(6.2, 5.8)])

    # Merge into consensus
    fc.add_arrow("reweight", "consensus", from_port="bottom", to_port="top", waypoints=[(1.8, 3.6), (4.0, 3.6)])
    fc.add_arrow("nominal", "consensus", from_port="bottom", to_port="top", waypoints=[(6.2, 3.6), (4.0, 3.6)])

    fc.add_arrow("consensus", "actuation")
    fc.add_arrow("actuation", "end")

    primary = out_paths[0]
    os.makedirs(os.path.dirname(primary), exist_ok=True)
    fc.render(primary, close_fig=True)
    distribute_file(primary, out_paths)
    print("Flowchart 1 rendered successfully!")


def make_flowchart2(out_paths):
    """Flowchart 2: Information-Geometric Event-Triggered Communication (IG-ETC)"""
    fc = ButterFlowchart(
        title="Flowchart 2: Information-Geometric Event-Triggered Communication (IG-ETC)",
        width=8.0, height=11.2
    )

    # 1. Start Capsule
    fc.add_node("start", "Belief State Ingestion", shape_type="capsule",
                x=4.0, y=10.0, width=4.6, height=0.75, icon="sensor",
                subtitle="Local EKF Distribution: p_i(t) = N(μ_i, Σ_i)")

    # 2. Metric Evaluation Box
    fc.add_node("fisher", "Compute Fisher-Rao Geodesic", shape_type="box",
                x=4.0, y=8.7, width=4.6, height=0.75, icon="sheaf",
                subtitle="d_FR^2(p_i(t), p_i(t_last)) on P_+^6 Manifold")

    # 3. Dynamic Threshold Box
    fc.add_node("thresh", "Evaluate Dynamic Threshold", shape_type="box",
                x=4.0, y=7.4, width=4.6, height=0.75, icon="shield",
                subtitle="δ_i(t) = δ_0 exp(β_E(1-E_i(t)))(1+β_γ(1-γ_i(t)))")

    # 4. Trigger Decision Diamond
    fc.add_node("trig_dec", "Trigger Condition Met?\nd_FR(p_i, p_last) ≥ δ_i(t)", shape_type="diamond",
                x=4.0, y=5.8, width=4.2, height=1.1, icon="decision")

    # 5a. Broadcast Box (Left branch - Triggered)
    fc.add_node("broadcast", "RF Packet Broadcast", shape_type="box",
                x=1.8, y=4.4, width=3.0, height=0.75, icon="drone",
                subtitle="Transmit State & Reset t_last = t")

    # 5b. Silent Box (Right branch - Suppressed)
    fc.add_node("silence", "Radio Silence Mode", shape_type="box",
                x=6.2, y=4.4, width=3.0, height=0.75, icon="shield",
                subtitle="Save 79.7% Bandwidth; Dead-Reckon")

    # 6. Synchronization Box
    fc.add_node("sync", "Neighbor Tracking Sync", shape_type="box",
                x=4.0, y=3.0, width=4.6, height=0.75, icon="sheaf",
                subtitle="Update Shared Inter-Agent Belief Graph")

    # 7. Next Cycle Box
    fc.add_node("cycle", "Advance Discrete Clock", shape_type="box",
                x=4.0, y=1.8, width=4.6, height=0.75, icon="sensor",
                subtitle="t ← t + Δt (100 Hz State Loop)")

    # 8. End Capsule
    fc.add_node("end", "Cycle Complete / Standby", shape_type="capsule",
                x=4.0, y=0.7, width=4.6, height=0.75, icon="target",
                subtitle="Await Next Observation Sample")

    # Connect with crisp black arrows
    fc.add_arrow("start", "fisher")
    fc.add_arrow("fisher", "thresh")
    fc.add_arrow("thresh", "trig_dec")

    # Branches from decision
    fc.add_arrow("trig_dec", "broadcast", label="Yes (Trigger)", label_offset=(-0.25, 0.1),
                 from_port="left", to_port="top", waypoints=[(1.8, 5.8)])
    fc.add_arrow("trig_dec", "silence", label="No (Silence)", label_offset=(0.25, 0.1),
                 from_port="right", to_port="top", waypoints=[(6.2, 5.8)])

    # Merge into sync
    fc.add_arrow("broadcast", "sync", from_port="bottom", to_port="top", waypoints=[(1.8, 3.6), (4.0, 3.6)])
    fc.add_arrow("silence", "sync", from_port="bottom", to_port="top", waypoints=[(6.2, 3.6), (4.0, 3.6)])

    fc.add_arrow("sync", "cycle")
    fc.add_arrow("cycle", "end")

    primary = out_paths[0]
    os.makedirs(os.path.dirname(primary), exist_ok=True)
    fc.render(primary, close_fig=True)
    distribute_file(primary, out_paths)
    print("Flowchart 2 rendered successfully!")


def make_flowchart3(out_paths):
    """Flowchart 3: Decentralized SHATA Task Allocation & RTA Simplex Safety"""
    fc = ButterFlowchart(
        title="Flowchart 3: Decentralized SHATA Auction & RTA Simplex Safety",
        width=8.0, height=11.2
    )

    # 1. Start Capsule
    fc.add_node("start", "Mission Task Ingestion", shape_type="capsule",
                x=4.0, y=10.0, width=4.6, height=0.75, icon="target",
                subtitle="Target List & Dynamic Priority Queue")

    # 2. Bundle Construction Box
    fc.add_node("bundle", "SHATA Bundle Construction", shape_type="box",
                x=4.0, y=8.7, width=4.6, height=0.75, icon="drone",
                subtitle="Compute Marginal Bids: c_ij = Score(T_j | B_i)")

    # 3. Cochain Consensus Box
    fc.add_node("cochain", "Sheaf Cochain Consensus", shape_type="box",
                x=4.0, y=7.4, width=4.6, height=0.75, icon="sheaf",
                subtitle="Diffuse Winning Bid Vector y_i over Sheaf L_F")

    # 4. Outbid Check Diamond
    fc.add_node("outbid_dec", "Outbid Conflict Detected?\nWinner Discrepancy", shape_type="diamond",
                x=4.0, y=5.8, width=4.2, height=1.1, icon="decision")

    # 5a. Resolve Outbid Box (Left branch)
    fc.add_node("resolve", "Resolve Outbid / Rebidding", shape_type="box",
                x=1.8, y=4.4, width=3.0, height=0.75, icon="target",
                subtitle="Drop Outbid Tasks & Re-auction")

    # 5b. Confirm Box (Right branch)
    fc.add_node("confirm", "Confirm Bundle Assignment", shape_type="box",
                x=6.2, y=4.4, width=3.0, height=0.75, icon="sheaf",
                subtitle="Assign Valid Task Path a_i*")

    # 6. Safety Barrier Decision Diamond
    fc.add_node("safety_dec", "Safety Simplex CBF Check\nh(x) ≥ 0 Violated?", shape_type="diamond",
                x=4.0, y=3.0, width=4.2, height=1.1, icon="shield")

    # 7a. Fallback Safe Controller (Left branch)
    fc.add_node("fallback", "RTA Safe QP Fallback", shape_type="box",
                x=1.8, y=1.7, width=3.0, height=0.75, icon="shield",
                subtitle="Sub-1.2 ms Emergency Collision Avoidance")

    # 7b. Nominal Flight Controller (Right branch)
    fc.add_node("nominal_ctrl", "Nominal Flight Control", shape_type="box",
                x=6.2, y=1.7, width=3.0, height=0.75, icon="drone",
                subtitle="Nominal Trajectory Tracking u_nom")

    # 8. End Capsule
    fc.add_node("end", "Safe Motor Actuation", shape_type="capsule",
                x=4.0, y=0.6, width=4.6, height=0.65, icon="target",
                subtitle="PX4 Flight Execution with Zero Violations")

    # Connect with crisp black arrows
    fc.add_arrow("start", "bundle")
    fc.add_arrow("bundle", "cochain")
    fc.add_arrow("cochain", "outbid_dec")

    # Outbid branches
    fc.add_arrow("outbid_dec", "resolve", label="Yes", label_offset=(-0.15, 0.1),
                 from_port="left", to_port="top", waypoints=[(1.8, 5.8)])
    fc.add_arrow("outbid_dec", "confirm", label="No", label_offset=(0.15, 0.1),
                 from_port="right", to_port="top", waypoints=[(6.2, 5.8)])

    # From resolve loop back to bundle; from confirm go to safety check
    fc.add_arrow("resolve", "bundle", label="Re-bid", label_offset=(-0.25, 0),
                 from_port="left", to_port="left", waypoints=[(0.4, 4.4), (0.4, 8.7)])
    fc.add_arrow("confirm", "safety_dec", from_port="bottom", to_port="top",
                 waypoints=[(6.2, 3.8), (4.0, 3.8)])

    # Safety Simplex branches
    fc.add_arrow("safety_dec", "fallback", label="Yes (Risk)", label_offset=(-0.2, 0.1),
                 from_port="left", to_port="top", waypoints=[(1.8, 3.0)])
    fc.add_arrow("safety_dec", "nominal_ctrl", label="No (Safe)", label_offset=(0.2, 0.1),
                 from_port="right", to_port="top", waypoints=[(6.2, 3.0)])

    # Merge into actuation
    fc.add_arrow("fallback", "end", from_port="bottom", to_port="top",
                 waypoints=[(1.8, 1.0), (4.0, 1.0)])
    fc.add_arrow("nominal_ctrl", "end", from_port="bottom", to_port="top",
                 waypoints=[(6.2, 1.0), (4.0, 1.0)])

    primary = out_paths[0]
    os.makedirs(os.path.dirname(primary), exist_ok=True)
    fc.render(primary, close_fig=True)
    distribute_file(primary, out_paths)
    print("Flowchart 3 rendered successfully!")


if __name__ == "__main__":
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    fc1_targets = [
        os.path.join(workspace_root, "results", "plots", "fig_flowchart1_sheaf_coordination.png"),
        os.path.join(workspace_root, "submission_elseiver_(SWEVO)_RAS", "figures", "fig_flowchart1_sheaf_coordination.png"),
        os.path.join(workspace_root, "results", "fig_flowchart1_sheaf_coordination.png"),
        os.path.join(workspace_root, "Updated_significant", "figures", "fig_flowchart1_sheaf_coordination.png"),
        os.path.join(workspace_root, "Updated_significant", "manuscript", "figures", "fig_flowchart1_sheaf_coordination.png")
    ]

    fc2_targets = [
        os.path.join(workspace_root, "results", "plots", "fig_flowchart2_ig_etc.png"),
        os.path.join(workspace_root, "submission_elseiver_(SWEVO)_RAS", "figures", "fig_flowchart2_ig_etc.png"),
        os.path.join(workspace_root, "results", "fig_flowchart2_ig_etc.png"),
        os.path.join(workspace_root, "Updated_significant", "figures", "fig_flowchart2_ig_etc.png"),
        os.path.join(workspace_root, "Updated_significant", "manuscript", "figures", "fig_flowchart2_ig_etc.png")
    ]

    fc3_targets = [
        os.path.join(workspace_root, "results", "plots", "fig_flowchart3_shata_auction.png"),
        os.path.join(workspace_root, "submission_elseiver_(SWEVO)_RAS", "figures", "fig_flowchart3_shata_auction.png"),
        os.path.join(workspace_root, "results", "fig_flowchart3_shata_auction.png"),
        os.path.join(workspace_root, "Updated_significant", "figures", "fig_flowchart3_shata_auction.png"),
        os.path.join(workspace_root, "Updated_significant", "manuscript", "figures", "fig_flowchart3_shata_auction.png")
    ]

    make_flowchart1(fc1_targets)
    make_flowchart2(fc2_targets)
    make_flowchart3(fc3_targets)
    print("All 3 butterpy flowcharts rendered and distributed successfully!")
