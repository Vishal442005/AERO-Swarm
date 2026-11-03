"""
generate_simple_block_diagrams.py
Regenerates block diagrams for AERO-Swarm with ultra-simple styling:
- Strictly pure white box fills (zero colors)
- Solid black outlines (lw=1.5)
- Solid black arrows and connectors
- Crisp black typography
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle

def generate_simple_teaser(dest_paths):
    fig, ax = plt.subplots(figsize=(7.5, 3.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.5)
    ax.axis('off')

    # Leader Box - Pure white, black border
    bbox_leader = dict(boxstyle='round,pad=0.45', facecolor='white', edgecolor='black', lw=1.5)
    ax.text(2.0, 3.2, 'Leader UAV ($u \\in V_{\\mathrm{leader}}$)\nStalk: $\\mathcal{F}_u = \\mathbb{R}^{24}$\n(VIO-SLAM, 3D Cov, High Compute)', 
            ha='center', va='center', bbox=bbox_leader, fontsize=8.5, fontweight='bold', color='black')

    # Scout Box - Pure white, black border
    bbox_scout = dict(boxstyle='round,pad=0.45', facecolor='white', edgecolor='black', lw=1.5)
    ax.text(8.0, 3.2, 'Scout UAV ($v \\in V_{\\mathrm{scout}}$)\nStalk: $\\mathcal{F}_v = \\mathbb{R}^{12}$\n(Agile Camera, Lightweight IMU)', 
            ha='center', va='center', bbox=bbox_scout, fontsize=8.5, fontweight='bold', color='black')

    # Edge Stalk Box (Center) - Pure white, black border
    bbox_edge = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', lw=1.5)
    ax.text(5.0, 1.25, 'Edge Stalk: $\\mathcal{F}_e = \\mathbb{R}^6$\n(Shared Subspace: 3D Pos + 3D Vel)\nLink Integrity: $\\gamma_{uv}(t) \\in [0, 1]$\nDirichlet Energy: $\\|\\mathbf{P}_u \\mathbf{x}_u - \\mathbf{P}_v \\mathbf{x}_v\\|^2$', 
            ha='center', va='center', bbox=bbox_edge, fontsize=8.5, fontweight='bold', color='black')

    # Restriction arrows - Solid black
    ax.annotate('$\\mathbf{P}_{u \\trianglelefteq e} \\in \\mathbb{R}^{6 \\times 24}$\n(SE(3)-Equivariant)', 
                xy=(3.8, 1.7), xytext=(2.6, 2.4),
                arrowprops=dict(facecolor='black', edgecolor='black', width=1.5, headwidth=6, headlength=7, shrink=0.01),
                fontsize=8, fontweight='bold', ha='center', color='black')

    ax.annotate('$\\mathbf{P}_{v \\trianglelefteq e} \\in \\mathbb{R}^{6 \\times 12}$\n(SE(3)-Equivariant)', 
                xy=(6.2, 1.7), xytext=(7.4, 2.4),
                arrowprops=dict(facecolor='black', edgecolor='black', width=1.5, headwidth=6, headlength=7, shrink=0.01),
                fontsize=8, fontweight='bold', ha='center', color='black')

    # Jammer Threat Label (Clean black box)
    bbox_jam = dict(boxstyle='square,pad=0.3', facecolor='white', edgecolor='black', lw=1.2, linestyle='--')
    ax.text(5.0, 3.9, 'Adversarial RF Jamming ($P_{\\mathrm{jam}}$, Rayleigh Fading)', 
            ha='center', va='center', bbox=bbox_jam, fontsize=8.5, fontweight='bold', color='black')

    # Dashed jammer attenuation arrows - Solid black
    ax.annotate('', xy=(5.0, 2.3), xytext=(5.0, 3.5),
                arrowprops=dict(facecolor='black', edgecolor='black', width=1.2, headwidth=5.5, headlength=6, linestyle='--'))

    plt.tight_layout()
    for p in dest_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Simple teaser sheaf concept diagram generated successfully!")


def generate_simple_ros2_architecture(dest_paths):
    fig, ax = plt.subplots(figsize=(8.0, 3.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.2)
    ax.axis('off')

    b_style = dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', lw=1.5)
    b_sq = dict(boxstyle='square,pad=0.4', facecolor='white', edgecolor='black', lw=1.5)

    # Box 1: PX4 Autopilot SITL & Hardware
    ax.text(1.2, 2.1, 'PX4 Autopilot SITL\n(6-DoF Dynamics,\nIMU / ToF / VIO)\n[100 Hz]', 
            ha='center', va='center', bbox=b_sq, fontsize=8.0, fontweight='bold', color='black')

    # Box 2: State Estimator EKF
    ax.text(3.6, 3.2, 'State Estimator & EKF\nBelief: $p_i(t) = \\mathcal{N}(\\mu_i, \\Sigma_i)$\n[100 Hz]',
            ha='center', va='center', bbox=b_style, fontsize=8.0, fontweight='bold', color='black')

    # Box 3: IG-ETC Trigger Node
    ax.text(7.2, 3.2, 'IG-ETC Trigger Node\n$d_{\\mathrm{FR}}(p_i, p_{\\mathrm{last}}) \\geq \\delta_i(t)$\n[Event-Driven 5-20 Hz]',
            ha='center', va='center', bbox=b_style, fontsize=8.0, fontweight='bold', color='black')

    # Box 4: Sheaf Consensus Engine
    ax.text(7.2, 1.0, 'Sheaf Consensus & SCVI\n$\\mathbf{L}_\\mathcal{F} = \\mathbf{L}_{\\mathrm{Bochner}} + \\mathbf{Ric}_{\\mathrm{Forman}}$\n[20 Hz Consensus]',
            ha='center', va='center', bbox=b_style, fontsize=8.0, fontweight='bold', color='black')

    # Box 5: RTA Safety Simplex Monitor
    ax.text(3.6, 1.0, 'RTA Safety Simplex\n$\\dot{h} + \\alpha h \\geq 0$ (QP Override)\n<1.2 ms (SAE ARP4754B)',
            ha='center', va='center', bbox=b_style, fontsize=8.0, fontweight='bold', color='black')

    # Arrows - strictly black
    arr_prop = dict(facecolor='black', edgecolor='black', width=1.5, headwidth=5.5, headlength=6, shrink=0.01)
    
    # PX4 to EKF
    ax.annotate('', xy=(2.6, 3.2), xytext=(1.9, 2.4), arrowprops=arr_prop)
    # EKF to IG-ETC
    ax.annotate('', xy=(5.7, 3.2), xytext=(4.7, 3.2), arrowprops=arr_prop)
    # IG-ETC to Sheaf Consensus
    ax.annotate('', xy=(7.2, 1.8), xytext=(7.2, 2.4), arrowprops=arr_prop)
    # Sheaf Consensus to RTA Simplex
    ax.annotate('', xy=(4.9, 1.0), xytext=(5.6, 1.0), arrowprops=arr_prop)
    # RTA Simplex to PX4
    ax.annotate('', xy=(1.9, 1.7), xytext=(2.6, 1.0), arrowprops=arr_prop)

    # Labels for arrows
    lbl_style = dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='black', lw=0.7)
    ax.text(2.0, 2.9, 'IMU/VIO', fontsize=7.2, ha='center', va='center', bbox=lbl_style, color='black')
    ax.text(5.2, 3.45, 'Belief $p_i$', fontsize=7.2, ha='center', va='center', bbox=lbl_style, color='black')
    ax.text(7.9, 2.1, 'Event RF\nBroadcast', fontsize=7.2, ha='center', va='center', bbox=lbl_style, color='black')
    ax.text(5.25, 1.25, 'Desired $u_i^*$', fontsize=7.2, ha='center', va='center', bbox=lbl_style, color='black')
    ax.text(1.9, 1.2, 'Safe $u_i$', fontsize=7.2, ha='center', va='center', bbox=lbl_style, color='black')

    plt.tight_layout()
    for p in dest_paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        plt.savefig(p, dpi=300, bbox_inches='tight')
    plt.close()
    print("Simple ROS 2 architecture diagram generated successfully!")


if __name__ == '__main__':
    teaser_targets = [
        "/media/jarvis/01DB55B559EC9500/Robotics Swarm/results/plots/fig_teaser_sheaf_concept.png",
        "/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_ieee_(T-Cyb)/figures/fig_teaser_sheaf_concept.png",
        "/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_elseiver_(SWEVO)_RAS/figures/fig_teaser_sheaf_concept.png",
        "/home/jarvis/.gemini/antigravity/brain/fafe8fae-1dc3-4e8d-9de8-adc10005550e/fig_teaser_sheaf_concept.png"
    ]
    ros2_targets = [
        "/media/jarvis/01DB55B559EC9500/Robotics Swarm/results/plots/fig_ros2_architecture.png",
        "/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_ieee_(T-Cyb)/figures/fig_ros2_architecture.png",
        "/media/jarvis/01DB55B559EC9500/Robotics Swarm/submission_elseiver_(SWEVO)_RAS/figures/fig_ros2_architecture.png",
        "/home/jarvis/.gemini/antigravity/brain/fafe8fae-1dc3-4e8d-9de8-adc10005550e/fig_ros2_architecture.png"
    ]

    generate_simple_teaser(teaser_targets)
    generate_simple_ros2_architecture(ros2_targets)
