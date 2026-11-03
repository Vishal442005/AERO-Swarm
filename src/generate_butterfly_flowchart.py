"""
generate_butterfly_flowchart.py
Generates a publication-grade, high-resolution Butterfly Flowchart
for AERO-Swarm coordination and resilience in contested environments.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, PathPatch
import matplotlib.path as mpath
import numpy as np

def draw_drone_icon(ax, x, y, size=0.25, color="#1E293B"):
    # Center body
    ax.add_patch(Circle((x, y), size*0.35, facecolor=color, edgecolor="black", lw=1.2, zorder=10))
    # 4 arms
    d = size * 0.7
    ax.plot([x - d, x + d], [y - d, y + d], color="black", lw=2, zorder=9)
    ax.plot([x - d, x + d], [y + d, y - d], color="black", lw=2, zorder=9)
    # 4 rotors
    for dx, dy in [(-d, -d), (d, d), (-d, d), (d, -d)]:
        ax.add_patch(Circle((x + dx, y + dy), size*0.25, facecolor="#94A3B8", edgecolor="black", lw=1.2, zorder=10))

def draw_satellite_icon(ax, x, y, size=0.25):
    # Satellite body
    ax.add_patch(FancyBboxPatch((x - size*0.3, y - size*0.3), size*0.6, size*0.6,
                                boxstyle="round,pad=0.02", facecolor="#E2E8F0", edgecolor="black", lw=1.2, zorder=10))
    # Solar panels
    ax.add_patch(FancyBboxPatch((x - size*1.1, y - size*0.2), size*0.7, size*0.4,
                                boxstyle="square,pad=0", facecolor="#38BDF8", edgecolor="black", lw=1.2, zorder=10))
    ax.add_patch(FancyBboxPatch((x + size*0.4, y - size*0.2), size*0.7, size*0.4,
                                boxstyle="square,pad=0", facecolor="#38BDF8", edgecolor="black", lw=1.2, zorder=10))
    # Red cross for GPS-denied
    ax.plot([x - size*0.9, x + size*0.9], [y - size*0.6, y + size*0.6], color="#EF4444", lw=2.5, zorder=12)
    ax.plot([x - size*0.9, x + size*0.9], [y + size*0.6, y - size*0.6], color="#EF4444", lw=2.5, zorder=12)

def draw_jamming_icon(ax, x, y, size=0.25):
    # Antenna tower
    ax.plot([x, x], [y - size*0.8, y + size*0.3], color="black", lw=2, zorder=9)
    ax.plot([x - size*0.4, x + size*0.4], [y - size*0.8, y - size*0.8], color="black", lw=2, zorder=9)
    ax.plot([x - size*0.3, x], [y - size*0.8, y], color="black", lw=1.5, zorder=9)
    ax.plot([x + size*0.3, x], [y - size*0.8, y], color="black", lw=1.5, zorder=9)
    ax.add_patch(Circle((x, y + size*0.3), size*0.15, facecolor="#DC2626", edgecolor="black", lw=1.2, zorder=10))
    # Jamming waves
    for r in [size*0.45, size*0.75]:
        arc = patches.Arc((x, y + size*0.3), r*2, r*2, angle=0, theta1=30, theta2=150, color="#DC2626", lw=2, zorder=10)
        ax.add_patch(arc)

def draw_shield_icon(ax, x, y, size=0.25):
    # Shield shape
    verts = [
        (x - size*0.6, y + size*0.6),
        (x + size*0.6, y + size*0.6),
        (x + size*0.6, y - size*0.1),
        (x, y - size*0.8),
        (x - size*0.6, y - size*0.1),
    ]
    poly = patches.Polygon(verts, closed=True, facecolor="#10B981", edgecolor="black", lw=1.5, zorder=10)
    ax.add_patch(poly)
    # Check mark
    ax.plot([x - size*0.3, x - size*0.05, x + size*0.35], [y, y - size*0.3, y + size*0.3], color="white", lw=2.5, zorder=11)

def draw_target_icon(ax, x, y, size=0.25):
    # Target concentric rings
    ax.add_patch(Circle((x, y), size*0.7, facecolor="#FEE2E2", edgecolor="#DC2626", lw=1.5, zorder=9))
    ax.add_patch(Circle((x, y), size*0.45, facecolor="white", edgecolor="#DC2626", lw=1.5, zorder=10))
    ax.add_patch(Circle((x, y), size*0.2, facecolor="#DC2626", edgecolor="#DC2626", lw=1.2, zorder=11))

def draw_chip_icon(ax, x, y, size=0.25):
    # Central chip
    ax.add_patch(FancyBboxPatch((x - size*0.5, y - size*0.5), size, size,
                                boxstyle="square,pad=0", facecolor="#6366F1", edgecolor="black", lw=1.5, zorder=10))
    ax.text(x, y, "CORE", color="white", fontsize=7, fontweight="bold", ha="center", va="center", zorder=11)
    # Pins
    for offset in [-size*0.3, 0, size*0.3]:
        ax.plot([x + offset, x + offset], [y - size*0.5, y - size*0.75], color="black", lw=1.5, zorder=9)
        ax.plot([x + offset, x + offset], [y + size*0.5, y + size*0.75], color="black", lw=1.5, zorder=9)
        ax.plot([x - size*0.5, x - size*0.75], [y + offset, y + offset], color="black", lw=1.5, zorder=9)
        ax.plot([x + size*0.5, x + size*0.75], [y + offset, y + offset], color="black", lw=1.5, zorder=9)

def draw_arrow(ax, start, end, label=None, label_pos=0.5, label_offset=(0, 0.12)):
    x1, y1 = start
    x2, y2 = end
    ax.annotate(
        "", xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(facecolor="black", edgecolor="black", width=1.8, headwidth=7, headlength=7, shrink=0.01),
        zorder=5
    )
    if label:
        lx = x1 + (x2 - x1) * label_pos + label_offset[0]
        ly = y1 + (y2 - y1) * label_pos + label_offset[1]
        ax.text(lx, ly, label, fontsize=8, fontweight="bold", color="#1E293B", ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#CBD5E1", lw=0.8), zorder=8)

def create_butterfly_flowchart(save_path):
    fig, ax = plt.subplots(figsize=(16, 9), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Title Banner
    title_box = FancyBboxPatch((0.5, 8.2), 15.0, 0.65, boxstyle="round,pad=0.1",
                               facecolor="#0F172A", edgecolor="black", lw=1.5, zorder=2)
    ax.add_patch(title_box)
    ax.text(8.0, 8.52, "AERO-Swarm Butterfly Flowchart: Resilient Heterogeneous Swarm Architecture",
            color="white", fontsize=15, fontweight="bold", ha="center", va="center", zorder=3)

    # -------------------------------------------------------------
    # LEFT WING: INPUT DYNAMICS & THREAT VECTORS (CONVERGING INFLOW)
    # -------------------------------------------------------------
    # Left Wing Big Container
    left_wing = FancyBboxPatch((0.5, 0.6), 4.6, 7.3, boxstyle="round,pad=0.15",
                               facecolor="#F8FAFC", edgecolor="#3B82F6", lw=2.2, linestyle="--", zorder=1)
    ax.add_patch(left_wing)
    ax.text(2.8, 7.6, "LEFT WING: Inflow & Threat Inputs", color="#1D4ED8", fontsize=12, fontweight="bold", ha="center", va="center")

    # Box 1: Heterogeneous Fleets (Top Left)
    b1 = FancyBboxPatch((0.8, 5.4), 4.0, 1.8, boxstyle="round,pad=0.1",
                         facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5, zorder=2)
    ax.add_patch(b1)
    draw_drone_icon(ax, 1.25, 6.75, size=0.28, color="#2563EB")
    ax.text(2.8, 6.85, "1. Heterogeneous Aerial Fleet", fontsize=10, fontweight="bold", color="#1E3A8A", ha="center")
    fleet_text = "• Scouts (V_scout, d_v=12): ToF / Monocular\n• Leaders (V_leader, d_v=24): 3D LiDAR / VIO\n• Relays (V_relay, d_v=8): SDR Directional Mesh"
    ax.text(1.0, 6.0, fleet_text, fontsize=8.2, color="#1E293B", va="center")

    # Box 2: Sensory Belief State (Mid Left)
    b2 = FancyBboxPatch((0.8, 3.2), 4.0, 1.8, boxstyle="round,pad=0.1",
                         facecolor="#F0FDF4", edgecolor="#16A34A", lw=1.5, zorder=2)
    ax.add_patch(b2)
    draw_drone_icon(ax, 1.25, 4.55, size=0.28, color="#16A34A")
    ax.text(2.8, 4.65, "2. Distributed Belief Dynamics", fontsize=10, fontweight="bold", color="#14532D", ha="center")
    belief_text = "• Local Beliefs: p_i(t) ~ N(μ_i(t), Σ_i(t)) ∈ P_+^6\n• Covariance Geometry: Volumetric SLAM Ellipsoid\n• Battery Reserve: E_i(t) & Local Channel Quality γ_i"
    ax.text(1.0, 3.8, belief_text, fontsize=8.2, color="#1E293B", va="center")

    # Box 3: Contested Environment / Threats (Bottom Left)
    b3 = FancyBboxPatch((0.8, 1.0), 4.0, 1.8, boxstyle="round,pad=0.1",
                         facecolor="#FEF2F2", edgecolor="#DC2626", lw=1.5, zorder=2)
    ax.add_patch(b3)
    draw_satellite_icon(ax, 1.2, 2.35, size=0.22)
    draw_jamming_icon(ax, 1.9, 2.35, size=0.22)
    ax.text(3.1, 2.45, "3. Contested Threat Environment", fontsize=10, fontweight="bold", color="#991B1B", ha="center")
    threat_text = "• Active Directional EW Jamming Cones (0-80%)\n• GPS-Denied Canyons / Subterranean Tunnels\n• Sudden Physical Node Attrition (10-50% Loss)"
    ax.text(1.0, 1.6, threat_text, fontsize=8.2, color="#1E293B", va="center")


    # -------------------------------------------------------------
    # CENTRAL CORE: DECISION & MATHEMATICAL PIVOT ENGINE
    # -------------------------------------------------------------
    core_box = FancyBboxPatch((5.6, 0.6), 4.8, 7.3, boxstyle="round,pad=0.15",
                              facecolor="#FAF5FF", edgecolor="#7C3AED", lw=2.5, zorder=1)
    ax.add_patch(core_box)
    draw_chip_icon(ax, 8.0, 7.55, size=0.35)
    ax.text(8.0, 7.05, "CENTRAL PIVOT: AERO-Swarm Core Engine", color="#6D28D9", fontsize=11.5, fontweight="bold", ha="center", va="center")

    # Core Module A: Sheaf Restriction Kernel
    c_a = FancyBboxPatch((5.85, 5.0), 4.3, 1.7, boxstyle="round,pad=0.1",
                          facecolor="#EDE9FE", edgecolor="#8B5CF6", lw=1.4, zorder=2)
    ax.add_patch(c_a)
    ax.text(8.0, 6.35, "Cellular Sheaf Restriction Kernel", fontsize=9.5, fontweight="bold", color="#4C1D95", ha="center")
    ca_text = "• Resolves Asymmetric Stalks: F_v = R^{d_v} → F_e = R^6\n• SINR Adaptive Maps: ρ_{v⊴e}(t) = tanh(SINR/γ) P + σ W\n• Global Sheaf Laplacian: L_F = δ^* δ (PSD Block Matrix)"
    ax.text(6.0, 5.65, ca_text, fontsize=8.0, color="#1E293B", va="center")

    # Core Module B: Bochner Curvature Engine
    c_b = FancyBboxPatch((5.85, 3.0), 4.3, 1.7, boxstyle="round,pad=0.1",
                          facecolor="#F5F3FF", edgecolor="#7C3AED", lw=1.4, zorder=2)
    ax.add_patch(c_b)
    ax.text(8.0, 4.35, "Bochner-Weitzenböck Curvature (SCVI)", fontsize=9.5, fontweight="bold", color="#4C1D95", ha="center")
    cb_text = "• Decomposition: L_F = L_F^{Bochner} + Ric_F^{Forman}\n• Curvature Index: κ_v(t) = λ_{min}(Ric_F(v, t))\n• Theorem 2: Linear Decay SRI ≥ SRI_0(1 - c f_{jam})"
    ax.text(6.0, 3.65, cb_text, fontsize=8.0, color="#1E293B", va="center")

    # Core Module C: Fisher-Rao Event Triggering
    c_c = FancyBboxPatch((5.85, 1.0), 4.3, 1.7, boxstyle="round,pad=0.1",
                          facecolor="#EDE9FE", edgecolor="#8B5CF6", lw=1.4, zorder=2)
    ax.add_patch(c_c)
    ax.text(8.0, 2.35, "Fisher-Rao Riemannian Event-Trigger (IG-ETC)", fontsize=9.5, fontweight="bold", color="#4C1D95", ha="center")
    cc_text = "• Manifold Metric: d_{FR}^2(p_1, p_2) on Gaussian Beliefs\n• Energy-Annealed Gating: δ_i(E_i, γ_i) Threshold\n• 79.7% Bandwidth Cut: Transmit iff d_{FR} > δ_i"
    ax.text(6.0, 1.65, cc_text, fontsize=8.0, color="#1E293B", va="center")


    # -------------------------------------------------------------
    # RIGHT WING: DECENTRALIZED MULTI-BRANCH EXECUTION & RESILIENCE
    # -------------------------------------------------------------
    right_wing = FancyBboxPatch((10.9, 0.6), 4.6, 7.3, boxstyle="round,pad=0.15",
                                facecolor="#F8FAFC", edgecolor="#059669", lw=2.2, linestyle="--", zorder=1)
    ax.add_patch(right_wing)
    ax.text(13.2, 7.6, "RIGHT WING: Decentralized Execution & Safety", color="#047857", fontsize=12, fontweight="bold", ha="center", va="center")

    # Box 4: SHATA Distributed Auction (Top Right)
    b4 = FancyBboxPatch((11.2, 5.4), 4.0, 1.8, boxstyle="round,pad=0.1",
                         facecolor="#ECFDF5", edgecolor="#059669", lw=1.5, zorder=2)
    ax.add_patch(b4)
    draw_target_icon(ax, 11.65, 6.75, size=0.26)
    ax.text(13.2, 6.85, "4. SHATA Distributed Task Allocation", fontsize=10, fontweight="bold", color="#064E3B", ha="center")
    shata_text = "• Sheaf-Valued Bundle Construction: c_{im}(B_i)\n• Curvature-Guided Conflict Resolution over Cochains\n• Polynomial Complexity: O(|V| M D_G) Convergence"
    ax.text(11.4, 6.0, shata_text, fontsize=8.2, color="#1E293B", va="center")

    # Box 5: RTA Simplex Safety Gateway (Mid Right)
    b5 = FancyBboxPatch((11.2, 3.2), 4.0, 1.8, boxstyle="round,pad=0.1",
                         facecolor="#FEFCE8", edgecolor="#CA8A04", lw=1.5, zorder=2)
    ax.add_patch(b5)
    draw_shield_icon(ax, 11.65, 4.55, size=0.26)
    ax.text(13.2, 4.65, "5. Hardware RTA Safety Simplex", fontsize=10, fontweight="bold", color="#713F12", ha="center")
    rta_text = "• Online Barrier Monitor: h_{safe} = ||p_i - p_j||^2 - R_{col}^2\n• Sub-1.2 ms Certified Fallback Override\n• 0 Safety Violations: Guaranteed Invariance C"
    ax.text(11.4, 3.8, rta_text, fontsize=8.2, color="#1E293B", va="center")

    # Box 6: Flight Actuation & Mission Success (Bottom Right)
    b6 = FancyBboxPatch((11.2, 1.0), 4.0, 1.8, boxstyle="round,pad=0.1",
                         facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.5, zorder=2)
    ax.add_patch(b6)
    draw_drone_icon(ax, 11.65, 2.35, size=0.28, color="#059669")
    ax.text(13.2, 2.45, "6. Resilient Fleet Swarm Autonomy", fontsize=10, fontweight="bold", color="#1E3A8A", ha="center")
    res_text = "• SE(3) Trajectory Tracking via PX4 DDS Bridge (50 Hz)\n• >91.3% TCR Preserved under 60% Severe RF Jamming\n• Multi-Robot Scalability up to N=200 Drones (<14.2 ms)"
    ax.text(11.4, 1.6, res_text, fontsize=8.2, color="#1E293B", va="center")


    # -------------------------------------------------------------
    # BLACK FLOW ARROWS: INFLOW (LEFT -> CORE)
    # -------------------------------------------------------------
    # From Box 1 (Fleet) to Core A (Restriction Kernel)
    draw_arrow(ax, (4.8, 6.3), (5.85, 6.0), label="Stalk Mappings", label_pos=0.45)
    # From Box 2 (Belief) to Core C (Fisher-Rao)
    draw_arrow(ax, (4.8, 4.1), (5.85, 2.2), label="Belief Ellipsoids", label_pos=0.45)
    # From Box 3 (Threats) to Core B (Bochner SCVI)
    draw_arrow(ax, (4.8, 1.9), (5.85, 3.6), label="Jamming / SINR", label_pos=0.45)

    # Internal Core Interconnections
    draw_arrow(ax, (8.0, 5.0), (8.0, 4.7), label=None)
    draw_arrow(ax, (8.0, 3.0), (8.0, 2.7), label=None)

    # -------------------------------------------------------------
    # BLACK FLOW ARROWS: OUTFLOW (CORE -> RIGHT)
    # -------------------------------------------------------------
    # From Core B/A to Box 4 (SHATA Auction)
    draw_arrow(ax, (10.15, 5.8), (11.2, 6.3), label="Curvature Bids", label_pos=0.55)
    # From Core A to Box 5 (RTA Simplex)
    draw_arrow(ax, (10.15, 3.8), (11.2, 4.1), label="State Invariants", label_pos=0.55)
    # From Core C to Box 6 (Actuation / Swarm Autonomy)
    draw_arrow(ax, (10.15, 1.8), (11.2, 1.9), label="Triggered Setpoints", label_pos=0.55)

    # Vertical coordination right-wing flow
    draw_arrow(ax, (13.2, 5.4), (13.2, 5.0), label=None)
    draw_arrow(ax, (13.2, 3.2), (13.2, 2.8), label=None)

    # Bottom caption
    fig.text(0.5, 0.02,
             "Figure: Butterfly Flowchart Architecture for AERO-Swarm. Left wing captures multi-source heterogeneous platforms and adversarial EW stress; "
             "central core synthesizes Cellular Sheaf Laplacians, Bochner-Weitzenböck SCVI curvature, and Fisher-Rao event triggering; "
             "right wing executes distributed SHATA auctions, hardware-isolated RTA Simplex safety verification, and resilient PX4 flight control.",
             fontsize=8.5, ha="center", va="bottom", color="#334155", style="italic")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Butterfly flowchart saved successfully to {save_path}")

if __name__ == "__main__":
    create_butterfly_flowchart("/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_ieee_(T-Cyb)/figures/fig_butterfly_flowchart.png")
    create_butterfly_flowchart("/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_elseiver_(SWEVO)_RAS/figures/fig_butterfly_flowchart.png")
    create_butterfly_flowchart("/media/jarvis/01DB55B559EC9500/Robotics Swarm/results/fig_butterfly_flowchart.png")
