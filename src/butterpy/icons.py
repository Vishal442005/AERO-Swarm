"""
butterpy.icons
Minimalist black-and-white vector icons for clean publication flowcharts.
Strictly black outlines, white/transparent fills, zero color.
"""

import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

def draw_drone_icon(ax, x, y, size=0.22):
    # Minimalist quadrotor: center circle + 4 arms + 4 rotor rings
    ax.add_patch(Circle((x, y), size*0.35, facecolor="white", edgecolor="black", lw=1.4, zorder=10))
    d = size * 0.65
    ax.plot([x - d, x + d], [y - d, y + d], color="black", lw=1.4, zorder=9)
    ax.plot([x - d, x + d], [y + d, y - d], color="black", lw=1.4, zorder=9)
    for dx, dy in [(-d, -d), (d, d), (-d, d), (d, -d)]:
        ax.add_patch(Circle((x + dx, y + dy), size*0.22, facecolor="white", edgecolor="black", lw=1.2, zorder=10))

def draw_sensor_icon(ax, x, y, size=0.22):
    # Sensor radar/lens
    ax.add_patch(Circle((x, y), size*0.45, facecolor="white", edgecolor="black", lw=1.4, zorder=10))
    ax.add_patch(Circle((x, y), size*0.20, facecolor="black", edgecolor="black", lw=1.0, zorder=11))
    for angle in [-25, 0, 25]:
        rad = size * 0.8
        dx = rad * 0.75
        dy = rad * (angle / 25.0) * 0.4
        ax.plot([x + size*0.45, x + dx], [y, y + dy], color="black", lw=1.2, linestyle="--", zorder=9)

def draw_decision_icon(ax, x, y, size=0.20):
    # Crisp black question mark
    ax.text(x, y, "?", color="black", fontsize=11, fontweight="bold", ha="center", va="center", zorder=12)

def draw_sheaf_core_icon(ax, x, y, size=0.22):
    # Microprocessor / Laplacian symbol
    ax.add_patch(FancyBboxPatch((x - size*0.45, y - size*0.45), size*0.9, size*0.9,
                                boxstyle="square,pad=0", facecolor="white", edgecolor="black", lw=1.4, zorder=10))
    ax.text(x, y, "L", color="black", fontsize=8.5, fontweight="bold", ha="center", va="center", zorder=11)
    for offset in [-size*0.25, 0, size*0.25]:
        ax.plot([x + offset, x + offset], [y - size*0.45, y - size*0.62], color="black", lw=1.2, zorder=9)
        ax.plot([x + offset, x + offset], [y + size*0.45, y + size*0.62], color="black", lw=1.2, zorder=9)
        ax.plot([x - size*0.45, x - size*0.62], [y + offset, y + offset], color="black", lw=1.2, zorder=9)
        ax.plot([x + size*0.45, x + size*0.62], [y + offset, y + offset], color="black", lw=1.2, zorder=9)

def draw_target_icon(ax, x, y, size=0.22):
    # Concentric target circles
    ax.add_patch(Circle((x, y), size*0.55, facecolor="white", edgecolor="black", lw=1.4, zorder=10))
    ax.add_patch(Circle((x, y), size*0.32, facecolor="white", edgecolor="black", lw=1.2, zorder=11))
    ax.add_patch(Circle((x, y), size*0.12, facecolor="black", edgecolor="black", lw=1.0, zorder=12))

def draw_shield_icon(ax, x, y, size=0.22):
    # Safety barrier shield
    verts = [
        (x - size*0.5, y + size*0.5),
        (x + size*0.5, y + size*0.5),
        (x + size*0.5, y - size*0.1),
        (x, y - size*0.7),
        (x - size*0.5, y - size*0.1),
    ]
    poly = Polygon(verts, closed=True, facecolor="white", edgecolor="black", lw=1.4, zorder=10)
    ax.add_patch(poly)
    ax.plot([x - size*0.22, x - size*0.05, x + size*0.25], [y, y - size*0.22, y + size*0.22], color="black", lw=1.8, zorder=11)

def draw_jammer_tower_icon(ax, x, y, size=0.22):
    # Minimalist antenna tower with signal arcs
    ax.plot([x, x], [y - size*0.6, y + size*0.2], color="black", lw=1.6, zorder=9)
    ax.plot([x - size*0.3, x + size*0.3], [y - size*0.6, y - size*0.6], color="black", lw=1.6, zorder=9)
    ax.add_patch(Circle((x, y + size*0.2), size*0.12, facecolor="black", edgecolor="black", lw=1.0, zorder=10))
    for r in [size*0.35, size*0.6]:
        arc = patches.Arc((x, y + size*0.2), r*2, r*2, angle=0, theta1=20, theta2=160, color="black", lw=1.4, zorder=10)
        ax.add_patch(arc)
