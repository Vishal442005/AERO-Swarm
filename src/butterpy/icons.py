"""
butterpy.icons
Vector icon glyph drawing routines for butterpy flowchart extension.
"""

import matplotlib.patches as patches
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

def draw_drone_icon(ax, x, y, size=0.22, color="#1E293B"):
    # Center body
    ax.add_patch(Circle((x, y), size*0.35, facecolor=color, edgecolor="black", lw=1.2, zorder=10))
    d = size * 0.7
    # Arms
    ax.plot([x - d, x + d], [y - d, y + d], color="black", lw=1.8, zorder=9)
    ax.plot([x - d, x + d], [y + d, y - d], color="black", lw=1.8, zorder=9)
    # Rotors
    for dx, dy in [(-d, -d), (d, d), (-d, d), (d, -d)]:
        ax.add_patch(Circle((x + dx, y + dy), size*0.25, facecolor="#94A3B8", edgecolor="black", lw=1.0, zorder=10))

def draw_sensor_icon(ax, x, y, size=0.22):
    # Sensor lens / radar dish
    ax.add_patch(Circle((x, y), size*0.5, facecolor="#E0F2FE", edgecolor="#0284C7", lw=1.4, zorder=10))
    ax.add_patch(Circle((x, y), size*0.25, facecolor="#0284C7", edgecolor="black", lw=1.0, zorder=11))
    # Beams
    for angle in [-30, 0, 30]:
        rad = size * 0.9
        dx = rad * 0.8
        dy = rad * (angle / 30.0) * 0.5
        ax.plot([x + size*0.5, x + dx], [y, y + dy], color="#0284C7", lw=1.2, linestyle="--", zorder=9)

def draw_decision_icon(ax, x, y, size=0.20):
    # Scale or question icon
    ax.text(x, y, "?", color="#D97706", fontsize=11, fontweight="bold", ha="center", va="center", zorder=12)

def draw_sheaf_core_icon(ax, x, y, size=0.22):
    # CPU / Sheaf kernel chip
    ax.add_patch(FancyBboxPatch((x - size*0.45, y - size*0.45), size*0.9, size*0.9,
                                boxstyle="square,pad=0", facecolor="#7C3AED", edgecolor="black", lw=1.2, zorder=10))
    ax.text(x, y, "LF", color="white", fontsize=7.5, fontweight="bold", ha="center", va="center", zorder=11)
    # Pins
    for offset in [-size*0.25, 0, size*0.25]:
        ax.plot([x + offset, x + offset], [y - size*0.45, y - size*0.65], color="black", lw=1.2, zorder=9)
        ax.plot([x + offset, x + offset], [y + size*0.45, y + size*0.65], color="black", lw=1.2, zorder=9)
        ax.plot([x - size*0.45, x - size*0.65], [y + offset, y + offset], color="black", lw=1.2, zorder=9)
        ax.plot([x + size*0.45, x + size*0.65], [y + offset, y + offset], color="black", lw=1.2, zorder=9)

def draw_target_icon(ax, x, y, size=0.22):
    # Concentric target
    ax.add_patch(Circle((x, y), size*0.55, facecolor="#FEE2E2", edgecolor="#DC2626", lw=1.4, zorder=10))
    ax.add_patch(Circle((x, y), size*0.32, facecolor="white", edgecolor="#DC2626", lw=1.2, zorder=11))
    ax.add_patch(Circle((x, y), size*0.12, facecolor="#DC2626", edgecolor="#DC2626", lw=1.0, zorder=12))

def draw_shield_icon(ax, x, y, size=0.22):
    # Security shield
    verts = [
        (x - size*0.5, y + size*0.5),
        (x + size*0.5, y + size*0.5),
        (x + size*0.5, y - size*0.1),
        (x, y - size*0.7),
        (x - size*0.5, y - size*0.1),
    ]
    poly = Polygon(verts, closed=True, facecolor="#10B981", edgecolor="black", lw=1.4, zorder=10)
    ax.add_patch(poly)
    # White checkmark
    ax.plot([x - size*0.25, x - size*0.05, x + size*0.3], [y, y - size*0.25, y + size*0.25], color="white", lw=2.0, zorder=11)

def draw_jamming_tower_icon(ax, x, y, size=0.22):
    # Tower
    ax.plot([x, x], [y - size*0.6, y + size*0.2], color="black", lw=1.6, zorder=9)
    ax.plot([x - size*0.3, x + size*0.3], [y - size*0.6, y - size*0.6], color="black", lw=1.6, zorder=9)
    ax.add_patch(Circle((x, y + size*0.2), size*0.12, facecolor="#DC2626", edgecolor="black", lw=1.0, zorder=10))
    # Arcs
    for r in [size*0.35, size*0.6]:
        arc = patches.Arc((x, y + size*0.2), r*2, r*2, angle=0, theta1=20, theta2=160, color="#DC2626", lw=1.6, zorder=10)
        ax.add_patch(arc)
