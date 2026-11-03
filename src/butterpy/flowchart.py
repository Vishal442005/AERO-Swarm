"""
butterpy.flowchart
Core flowchart generation engine for butterpy extension.
Builds simple, publication-grade flowcharts with standard shapes (capsules, rectangles, diamonds),
crisp black arrows, readable text, and integrated domain graphics/icons.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon
from .icons import (
    draw_drone_icon, draw_sensor_icon, draw_decision_icon,
    draw_sheaf_core_icon, draw_target_icon, draw_shield_icon, draw_jamming_tower_icon
)

class Node:
    def __init__(self, node_id, text, shape_type="box", x=0, y=0, width=3.0, height=1.2, 
                 icon=None, color="#FFFFFF", border_color="#000000", lw=1.5, subtitle=None):
        self.node_id = node_id
        self.text = text
        self.shape_type = shape_type # "capsule", "box", "diamond"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.icon = icon
        self.color = color
        self.border_color = border_color
        self.lw = lw
        self.subtitle = subtitle

class ButterFlowchart:
    def __init__(self, title="System Coordination Flowchart", width=15, height=10):
        self.title = title
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=300)
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.axis("off")
        self.nodes = {}
        self.connections = []

    def add_node(self, node_id, text, shape_type="box", x=0, y=0, width=3.2, height=1.1,
                 icon=None, color="#F8FAFC", border_color="#000000", lw=1.5, subtitle=None):
        node = Node(node_id, text, shape_type, x, y, width, height, icon, color, border_color, lw, subtitle)
        self.nodes[node_id] = node
        return node

    def add_arrow(self, from_id, to_id, label=None, label_offset=(0, 0), connection_style="direct", 
                  waypoints=None, arrow_color="black"):
        self.connections.append({
            "from": from_id,
            "to": to_id,
            "label": label,
            "label_offset": label_offset,
            "style": connection_style,
            "waypoints": waypoints,
            "color": arrow_color
        })

    def draw_shape(self, node):
        x, y, w, h = node.x, node.y, node.width, node.height
        
        if node.shape_type == "capsule": # Terminal (Start/End)
            patch = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.1,rounding_size=0.4",
                                   facecolor=node.color, edgecolor=node.border_color, lw=node.lw, zorder=3)
            self.ax.add_patch(patch)
        elif node.shape_type == "diamond": # Decision block
            verts = [
                (x, y + h*0.65),
                (x + w*0.55, y),
                (x, y - h*0.65),
                (x - w*0.55, y)
            ]
            poly = Polygon(verts, closed=True, facecolor=node.color, edgecolor=node.border_color, lw=node.lw, zorder=3)
            self.ax.add_patch(poly)
        else: # Standard rectangle box (Process step)
            patch = FancyBboxPatch((x - w/2, y - h/2), w, h,
                                   boxstyle="round,pad=0.08,rounding_size=0.15",
                                   facecolor=node.color, edgecolor=node.border_color, lw=node.lw, zorder=3)
            self.ax.add_patch(patch)

        # Draw icon if specified
        icon_x = x - w/2 + 0.35 if node.shape_type != "diamond" else x - w/2 + 0.45
        text_x = x + 0.15 if node.icon else x
        
        if node.icon == "drone":
            draw_drone_icon(self.ax, icon_x, y, size=0.22, color="#2563EB")
        elif node.icon == "sensor":
            draw_sensor_icon(self.ax, icon_x, y, size=0.20)
        elif node.icon == "decision":
            draw_decision_icon(self.ax, icon_x, y, size=0.18)
        elif node.icon == "sheaf":
            draw_sheaf_core_icon(self.ax, icon_x, y, size=0.22)
        elif node.icon == "target":
            draw_target_icon(self.ax, icon_x, y, size=0.20)
        elif node.icon == "shield":
            draw_shield_icon(self.ax, icon_x, y, size=0.20)
        elif node.icon == "jammer":
            draw_jamming_tower_icon(self.ax, icon_x, y, size=0.20)

        # Draw text
        if node.subtitle:
            self.ax.text(text_x, y + 0.14, node.text, fontsize=9.2, fontweight="bold", 
                         color="#0F172A", ha="center", va="center", zorder=5)
            self.ax.text(text_x, y - 0.20, node.subtitle, fontsize=7.6, 
                         color="#334155", ha="center", va="center", zorder=5)
        else:
            self.ax.text(text_x, y, node.text, fontsize=9.2, fontweight="bold", 
                         color="#0F172A", ha="center", va="center", zorder=5)

    def draw_connections(self):
        for conn in self.connections:
            n1 = self.nodes[conn["from"]]
            n2 = self.nodes[conn["to"]]
            color = conn["color"]
            
            if conn.get("waypoints"):
                # Multi-segment line with arrow at end
                pts = [(n1.x, n1.y)] + conn["waypoints"] + [(n2.x, n2.y)]
                for i in range(len(pts) - 2):
                    self.ax.plot([pts[i][0], pts[i+1][0]], [pts[i][1], pts[i+1][1]], color=color, lw=1.8, zorder=2)
                # Last segment with annotation arrow
                self.ax.annotate(
                    "", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.8, headwidth=6.5, headlength=7, shrink=0.01),
                    zorder=2
                )
            else:
                # Direct arrow between nodes
                self.ax.annotate(
                    "", xy=(n2.x, n2.y), xytext=(n1.x, n1.y),
                    arrowprops=dict(facecolor=color, edgecolor=color, width=1.8, headwidth=6.5, headlength=7, shrink=0.01),
                    zorder=2
                )
            
            if conn["label"]:
                lx = (n1.x + n2.x) / 2.0 + conn["label_offset"][0]
                ly = (n1.y + n2.y) / 2.0 + conn["label_offset"][1]
                self.ax.text(lx, ly, conn["label"], fontsize=8.2, fontweight="bold",
                             color="#0F172A", ha="center", va="center",
                             bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#94A3B8", lw=0.8),
                             zorder=6)

    def render(self, output_path):
        # Draw Title Banner
        title_box = FancyBboxPatch((0.5, 9.1), 14.0, 0.65, boxstyle="round,pad=0.08",
                                   facecolor="#0F172A", edgecolor="black", lw=1.5, zorder=2)
        self.ax.add_patch(title_box)
        self.ax.text(7.5, 9.42, self.title, color="white", fontsize=13.5, fontweight="bold", ha="center", va="center", zorder=3)

        # Draw all connections first
        self.draw_connections()

        # Draw all nodes
        for node in self.nodes.values():
            self.draw_shape(node)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Flowchart successfully rendered and saved to {output_path}")
