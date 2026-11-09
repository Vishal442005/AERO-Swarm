"""
generate_publication_diagrams.py
Regenerates multi-panel, publication-grade figures for AERO-Swarm:
1. Figure 1 (fig_teaser_sheaf_concept.png): 4 panels (a), (b), (c), (d)
2. Figure 4 (fig_ros2_architecture.png): 2 panels (a), (b)
Styling: Clean black-and-white publication line art with grayscale accents,
crisp typography, exact subpanel labeling matching the captions.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Polygon

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams['font.family'] = 'DejaVu Sans'

def generate_teaser_4panel(dest_paths):
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.2), dpi=300)
    plt.subplots_adjust(wspace=0.18, hspace=0.25)

    # ----------------------------------------------------
    # Panel (a): Contested Tactical Canyon & RF Jammer
    # ----------------------------------------------------
    ax = axes[0, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Canyon walls (hatched polygons)
    canyon_left = Polygon([(0, 0), (2.2, 0), (2.8, 6.0), (1.5, 10), (0, 10)], 
                          facecolor='#e0e0e0', edgecolor='black', hatch='//', lw=1.2)
    canyon_right = Polygon([(7.8, 0), (10, 0), (10, 10), (8.5, 10), (7.2, 5.0)], 
                           facecolor='#e0e0e0', edgecolor='black', hatch='\\\\', lw=1.2)
    ax.add_patch(canyon_left)
    ax.add_patch(canyon_right)
    
    # Adversarial Jammer
    ax.plot(8.8, 7.5, 's', color='black', markersize=9)
    ax.text(8.8, 8.4, 'Adversarial\nEW Jammer', ha='center', va='bottom', fontsize=8, fontweight='bold')
    # Jamming wedge
    jam_cone = Polygon([(8.8, 7.5), (3.5, 5.2), (4.5, 1.8)], facecolor='#ffcccc', edgecolor='black', linestyle='--', alpha=0.5, lw=1.2)
    ax.add_patch(jam_cone)
    ax.text(6.6, 5.2, 'RF Jamming Cone\n($P_{\\mathrm{jam}}$, Rayleigh Fading)', fontsize=7.5, color='#990000', fontweight='bold', rotation=-22)

    # Drones inside canyon
    ax.plot(3.8, 7.8, 'o', color='black', markersize=7) # Leader
    ax.text(3.8, 8.4, 'Leader $u$', fontsize=8, fontweight='bold', ha='center')
    ax.plot(4.5, 4.2, '^', color='black', markersize=7) # Scout
    ax.text(4.5, 3.4, 'Scout $v$', fontsize=8, fontweight='bold', ha='center')
    ax.plot(6.2, 7.2, 'D', color='black', markersize=6) # Relay
    ax.text(6.2, 7.9, 'Relay $r$', fontsize=8, fontweight='bold', ha='center')

    # GPS Denied banner
    ax.text(5.0, 9.4, 'GPS-Denied Tactical Airspace (No GNSS)', ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='black', lw=1.1), fontsize=8.5, fontweight='bold')
    
    # Subpanel Label
    ax.text(0.2, 9.6, '(a)', fontsize=11, fontweight='bold', bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='black', lw=1.0))
    ax.set_title('(a) Contested Tactical 3D Environment', fontsize=9.5, fontweight='bold', y=-0.12)

    # ----------------------------------------------------
    # Panel (b): Classical Flat Graph Failure
    # ----------------------------------------------------
    ax = axes[0, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    b_node = dict(boxstyle='circle,pad=0.3', facecolor='white', edgecolor='black', lw=1.4)
    ax.text(2.2, 7.2, '$v_1$', ha='center', va='center', bbox=b_node, fontsize=9, fontweight='bold')
    ax.text(2.2, 2.8, '$v_2$', ha='center', va='center', bbox=b_node, fontsize=9, fontweight='bold')
    ax.text(7.8, 7.2, '$v_3$', ha='center', va='center', bbox=b_node, fontsize=9, fontweight='bold')
    ax.text(7.8, 2.8, '$v_4$', ha='center', va='center', bbox=b_node, fontsize=9, fontweight='bold')

    # Solid edge
    ax.annotate('', xy=(2.2, 3.8), xytext=(2.2, 6.2), arrowprops=dict(facecolor='black', edgecolor='black', width=1.5, headwidth=6))
    ax.text(1.2, 5.0, '$A_{12}=1$', fontsize=8, fontweight='bold', ha='center')
    ax.annotate('', xy=(7.8, 3.8), xytext=(7.8, 6.2), arrowprops=dict(facecolor='black', edgecolor='black', width=1.5, headwidth=6))
    ax.text(8.8, 5.0, '$A_{34}=1$', fontsize=8, fontweight='bold', ha='center')

    # Severed / Jammed edges (red cross / dashed)
    ax.plot([3.2, 6.8], [7.2, 7.2], 'k--', lw=1.5)
    ax.text(5.0, 7.2, 'X', color='red', fontsize=16, fontweight='bold', ha='center', va='center')
    ax.plot([3.2, 6.8], [2.8, 2.8], 'k--', lw=1.5)
    ax.text(5.0, 2.8, 'X', color='red', fontsize=16, fontweight='bold', ha='center', va='center')

    # Explanation banner
    collapse_box = dict(boxstyle='round,pad=0.35', facecolor='#fff0f0', edgecolor='red', lw=1.3)
    ax.text(5.0, 5.0, 'Catastrophic Percolation Collapse\n$\\lambda_2(\\mathbf{L}_G) \\to 0$ at $f_{\\mathrm{jam}} \\approx 0.35$\nScalar Graph Disconnects!',
            ha='center', va='center', bbox=collapse_box, fontsize=8.5, fontweight='bold', color='#990000')

    ax.text(0.2, 9.6, '(b)', fontsize=11, fontweight='bold', bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='black', lw=1.0))
    ax.set_title('(b) Classical Flat Graph Percolation Collapse', fontsize=9.5, fontweight='bold', y=-0.12)

    # ----------------------------------------------------
    # Panel (c): Cellular Sheaf Architecture
    # ----------------------------------------------------
    ax = axes[1, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    b_box = dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor='black', lw=1.3)
    # Leader
    ax.text(1.8, 8.0, 'Leader ($u$)\n$\\mathcal{F}_u = \\mathbb{R}^{24}$\n(VIO/SLAM)', ha='center', va='center', bbox=b_box, fontsize=7.5, fontweight='bold')
    # Scout
    ax.text(8.2, 8.0, 'Scout ($v$)\n$\\mathcal{F}_v = \\mathbb{R}^{12}$\n(Agile FoV)', ha='center', va='center', bbox=b_box, fontsize=7.5, fontweight='bold')
    # Relay
    ax.text(5.0, 1.8, 'Relay ($r$)\n$\\mathcal{F}_r = \\mathbb{R}^8$\n(SDR Mesh)', ha='center', va='center', bbox=b_box, fontsize=7.5, fontweight='bold')

    # Central Edge Stalk
    b_edge = dict(boxstyle='round,pad=0.4', facecolor='#f8f8f8', edgecolor='black', lw=1.4)
    ax.text(5.0, 5.4, 'Edge Stalk: $\\mathcal{F}_e = \\mathbb{R}^6$\nShared 3D Pos + 3D Vel\nCoboundary: $(\\delta x)_e = \\rho_{v \\trianglelefteq e} x_v - \\rho_{u \\trianglelefteq e} x_u$', 
            ha='center', va='center', bbox=b_edge, fontsize=7.5, fontweight='bold')

    # Arrows with restriction maps
    arr = dict(facecolor='black', edgecolor='black', width=1.3, headwidth=5.5, headlength=6, shrink=0.02)
    ax.annotate('', xy=(3.6, 5.8), xytext=(2.6, 7.0), arrowprops=arr)
    ax.text(2.6, 6.4, '$\\rho_{u \\to e} \\in \\mathbb{R}^{6 \\times 24}$', fontsize=7.5, fontweight='bold', color='black')

    ax.annotate('', xy=(6.4, 5.8), xytext=(7.4, 7.0), arrowprops=arr)
    ax.text(7.4, 6.4, '$\\rho_{v \\to e} \\in \\mathbb{R}^{6 \\times 12}$', fontsize=7.5, fontweight='bold', color='black')

    ax.annotate('', xy=(5.0, 4.3), xytext=(5.0, 2.9), arrowprops=arr)
    ax.text(5.6, 3.4, '$\\rho_{r \\to e} \\in \\mathbb{R}^{6 \\times 8}$', fontsize=7.5, fontweight='bold', color='black')

    ax.text(0.2, 9.6, '(c)', fontsize=11, fontweight='bold', bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='black', lw=1.0))
    ax.set_title('(c) Proposed Cellular Sheaf Paradigm $\\mathcal{F}$', fontsize=9.5, fontweight='bold', y=-0.12)

    # ----------------------------------------------------
    # Panel (d): Bochner-Weitzenböck Curvature & SCVI
    # ----------------------------------------------------
    ax = axes[1, 1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    decomp_box = dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', lw=1.4)
    ax.text(5.0, 8.2, 'Bochner-Weitzenboeck Decomposition:\n$\\mathbf{L}_F = \\mathbf{L}_F^{\\mathrm{Bochner}} + \\mathbf{Ric}_F^{\\mathrm{Forman}}$', 
            ha='center', va='center', bbox=decomp_box, fontsize=8.0, fontweight='bold')

    scvi_box = dict(boxstyle='round,pad=0.4', facecolor='#f0f4ff', edgecolor='blue', lw=1.2)
    ax.text(5.0, 5.2, 'Sheaf Curvature Vulnerability Index (SCVI):\n$\\kappa_v(t) = \\lambda_{\\min}(\\mathbf{Ric}_F(v, t))$\n'
                      '$\\bullet$ Attenuated SINR $\\rightarrow \\kappa_v < 0$ (Bottleneck Alert)\n'
                      '$\\bullet$ Early Warning BEFORE physical link severance', 
            ha='center', va='center', bbox=scvi_box, fontsize=8.0, fontweight='bold', color='#001166')

    resil_box = dict(boxstyle='square,pad=0.35', facecolor='white', edgecolor='black', lw=1.2)
    ax.text(5.0, 2.0, 'Resilience Guarantee (Theorem 1):\n$\\mathrm{SRI}(f_{\\mathrm{jam}}) \\geq \\mathrm{SRI}_0 (1 - c_F \\cdot f_{\\mathrm{jam}})$\nStrictly Linear Decay | Zero Percolation Threshold',
            ha='center', va='center', bbox=resil_box, fontsize=8.0, fontweight='bold')

    ax.text(0.2, 9.6, '(d)', fontsize=11, fontweight='bold', bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='black', lw=1.0))
    ax.set_title('(d) Bochner Curvature SCVI & Linear Resilience', fontsize=9.5, fontweight='bold', y=-0.12)

    plt.tight_layout()
    for p in dest_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated 4-panel Teaser Figure 1 successfully!")


def generate_ros2_architecture_2panel(dest_paths):
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), dpi=300)
    plt.subplots_adjust(wspace=0.20)

    # ----------------------------------------------------
    # Panel (a): ROS 2 Node Architecture
    # ----------------------------------------------------
    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    b_node = dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', lw=1.4)
    b_sitl = dict(boxstyle='square,pad=0.4', facecolor='#f5f5f5', edgecolor='black', lw=1.4)

    # 3 ROS 2 Nodes
    ax.text(5.0, 8.4, '1. aero_sheaf_coordinator\n(Stalks $\\mathcal{F}_v$, Bochner Curvature, /swarm/scvi_status)',
            ha='center', va='center', bbox=b_node, fontsize=7.8, fontweight='bold')
    
    ax.text(5.0, 5.8, '2. aero_task_allocator\n(SHATA Auction, Bundle Bidding, /swarm/task_bundles)',
            ha='center', va='center', bbox=b_node, fontsize=7.8, fontweight='bold')

    ax.text(5.0, 3.2, '3. aero_formation_controller\n(50 Hz Sheaf Consensus, SE(3) Setpoints, /swarm/cmd_vel)',
            ha='center', va='center', bbox=b_node, fontsize=7.8, fontweight='bold')

    # PX4 Autopilot SITL (Correctly spelled SITL!)
    ax.text(5.0, 0.9, 'PX4 Autopilot SITL & Hardware\n(micro-XRCE-DDS Bridge, MAVLink Actuator PWMs)',
            ha='center', va='center', bbox=b_sitl, fontsize=8.0, fontweight='bold')

    # Arrows between nodes
    arr = dict(facecolor='black', edgecolor='black', width=1.3, headwidth=5.5, headlength=6, shrink=0.02)
    ax.annotate('', xy=(5.0, 6.7), xytext=(5.0, 7.5), arrowprops=arr)
    ax.text(5.1, 7.1, 'SCVI Weight $\\kappa_v$', fontsize=7.0, ha='left')

    ax.annotate('', xy=(5.0, 4.1), xytext=(5.0, 4.9), arrowprops=arr)
    ax.text(5.1, 4.5, 'Assigned Bundles', fontsize=7.0, ha='left')

    ax.annotate('', xy=(5.0, 1.8), xytext=(5.0, 2.3), arrowprops=arr)
    ax.text(5.1, 2.05, 'DDS Bridge', fontsize=7.0, ha='left')

    ax.text(0.2, 9.5, '(a)', fontsize=11, fontweight='bold', bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='black', lw=1.0))
    ax.set_title('(a) Layered ROS 2 Humble Node Pipeline', fontsize=9.5, fontweight='bold', y=-0.10)

    # ----------------------------------------------------
    # Panel (b): Hardware-Isolated RTA Simplex Monitor
    # ----------------------------------------------------
    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    b_ai = dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor='black', lw=1.3)
    b_cbf = dict(boxstyle='round,pad=0.35', facecolor='#fbfbfb', edgecolor='black', lw=1.3)
    b_fall = dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor='black', lw=1.3)
    b_mux = dict(boxstyle='square,pad=0.4', facecolor='#fff0f0', edgecolor='red', lw=1.5)
    b_act = dict(boxstyle='square,pad=0.4', facecolor='#f5f5f5', edgecolor='black', lw=1.4)

    # Top: Complex AI Controller
    ax.text(2.6, 7.8, 'Complex AI Policy\n(Sheaf Consensus +\nNeural Motion Planner)',
            ha='center', va='center', bbox=b_ai, fontsize=7.8, fontweight='bold')

    # Middle: Safety Monitor
    ax.text(2.6, 4.8, 'CBF Safety Monitor\n$h_{\\mathrm{safe}}(x) = \\|p_i - p_j\\|^2 - R^2 \\geq 0$\n$\\dot{h} + \\alpha(h) \\geq 0$',
            ha='center', va='center', bbox=b_cbf, fontsize=7.8, fontweight='bold')

    # Bottom: Certified Fallback Controller
    ax.text(2.6, 1.8, 'Certified Fallback Controller\n(Provably Verified QP Braking\n& Collision Avoidance)',
            ha='center', va='center', bbox=b_fall, fontsize=7.8, fontweight='bold')

    # Right: Hardware Watchdog Multiplexer
    ax.text(7.6, 4.8, 'Hardware Watchdog\nSimplex Mux\n(<1.2 ms Override\nSAE ARP4754B)',
            ha='center', va='center', bbox=b_mux, fontsize=8.0, fontweight='bold', color='#990000')

    # Far Right: Actuators
    ax.text(7.6, 1.5, 'Safe Actuator PWMs\n(PX4 Motors)',
            ha='center', va='center', bbox=b_act, fontsize=8.0, fontweight='bold')

    # Arrows
    ax.annotate('', xy=(6.0, 6.0), xytext=(4.3, 7.8), arrowprops=arr)
    ax.text(5.0, 7.3, 'Nominal $u_{\\mathrm{AI}}$', fontsize=7.2)

    ax.annotate('', xy=(6.0, 4.8), xytext=(4.4, 4.8), arrowprops=arr)
    ax.text(5.0, 5.1, 'Trip Flag', fontsize=7.2, color='red')

    ax.annotate('', xy=(6.0, 3.6), xytext=(4.3, 1.8), arrowprops=arr)
    ax.text(5.0, 2.5, 'Fallback $u_{\\mathrm{safe}}$', fontsize=7.2)

    ax.annotate('', xy=(7.6, 2.4), xytext=(7.6, 3.4), arrowprops=arr)
    ax.text(7.7, 2.9, 'Guaranteed Safe $u^*$', fontsize=7.2, fontweight='bold')

    ax.text(0.2, 9.5, '(b)', fontsize=11, fontweight='bold', bbox=dict(boxstyle='square,pad=0.2', facecolor='white', edgecolor='black', lw=1.0))
    ax.set_title('(b) Hardware-Isolated RTA Simplex Architecture', fontsize=9.5, fontweight='bold', y=-0.10)

    plt.tight_layout()
    for p in dest_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated 2-panel ROS 2 Architecture Figure 4 successfully!")


if __name__ == '__main__':
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    teaser_targets = [
        os.path.join(workspace_root, "results", "plots", "fig_teaser_sheaf_concept.png"),
        os.path.join(workspace_root, "submission_elseiver_(SWEVO)_RAS", "figures", "fig_teaser_sheaf_concept.png"),
        os.path.join(workspace_root, "Updated_significant", "figures", "fig_teaser_sheaf_concept.png")
    ]
    ros2_targets = [
        os.path.join(workspace_root, "results", "plots", "fig_ros2_architecture.png"),
        os.path.join(workspace_root, "submission_elseiver_(SWEVO)_RAS", "figures", "fig_ros2_architecture.png"),
        os.path.join(workspace_root, "Updated_significant", "figures", "fig_ros2_architecture.png")
    ]

    generate_teaser_4panel(teaser_targets)
    generate_ros2_architecture_2panel(ros2_targets)
