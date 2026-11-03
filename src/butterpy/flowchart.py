"""
butterpy.flowchart
Minimalist flowchart engine for Python.
Generates ultra-simple, publication-grade flowcharts:
- Pure white box fills (strictly no colors inside boxes)
- Solid black borders and pure black arrows
- Crisp black typography
- Clean black-and-white line-art vector icons
- Simple shapes: Capsule (terminal), Rectangle (process), Diamond (decision)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Polygon
from .icons import (
    draw_drone_icon, draw_sensor_icon, draw_decision_icon,
    draw_sheaf_core_icon, draw_target_icon, draw_shield_icon, draw_jammer_tower_icon
)

class Node:
    def __init__(self, node_id, text, shape_type="box", x=0.0, y=0.0, width=3.4, height=0.9, 
                 icon=None, subtitle=None):
        self.node_id = node_id
        self.text = text
        self.shape_type = shape_type  # "capsule", "box", "diamond"
        self.x = float(x)
        self.y = float(y)
        self.width = float(width)
        self.height = float(height)
        self.icon = icon
        self.subtitle = subtitle

    def get_port(self, port_name):
        w, h = self.width, self.height
        if self.shape_type == "diamond":
            ports = {
                "top": (self.x, self.y + h * 0.62),
                "bottom": (self.x, self.y - h * 0.62),
                "left": (self.x - w * 0.55, self.y),
                "right": (self.x + w * 0.55, self.y),
            }
        else:
            ports = {
                "top": (self.x, self.y + h / 2.0),
                "bottom": (self.x, self.y - h / 2.0),
                "left": (self.x - w / 2.0, self.y),
                "right": (self.x + w / 2.0, self.y),
            }
        return ports.get(port_name, (self.x, self.y))


class ButterFlowchart:
    def __init__(self, title=None, width=8.5, height=10.0):
        self.title = title
        self.width = float(width)
        self.height = float(height)
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=300)
        self.ax.set_xlim(0, width)
        self.ax.set_ylim(0, height)
        self.ax.axis("off")
        self.nodes = {}
        self.connections = []

    def add_node(self, node_id, text, shape_type="box", x=0.0, y=0.0, width=3.4, height=0.9,
                 icon=None, subtitle=None):
        node = Node(node_id, text, shape_type, x, y, width, height, icon, subtitle)
        self.nodes[node_id] = node
        return node

    def add_arrow(self, from_id, to_id, label=None, label_offset=(0, 0),
                  from_port=None, to_port=None, waypoints=None):
        self.connections.append({
            "from": from_id,
            "to": to_id,
            "label": label,
            "label_offset": label_offset,
            "from_port": from_port,
            "to_port": to_port,
            "waypoints": waypoints
        })

    def _auto_ports(self, n1, n2):
        dx = n2.x - n1.x
        dy = n2.y - n1.y
        if abs(dy) >= abs(dx):
            if dy < 0:
                return "bottom", "top"
            else:
                return "top", "bottom"
        else:
            if dx > 0:
                return "right", "left"
            else:
                return "left", "right"

    def draw_shape(self, node):
        x, y, w, h = node.x, node.y, node.width, node.height
        
        # All shapes: pure white fill, solid crisp black border
        if node.shape_type == "capsule":  # Start / End
            patch = FancyBboxPatch((x - w/2.0, y - h/2.0), w, h,
                                   boxstyle="round,pad=0.08,rounding_size=0.35",
                                   facecolor="white", edgecolor="black", lw=1.5, zorder=3)
            self.ax.add_patch(patch)
        elif node.shape_type == "diamond":  # Decision
            verts = [
                (x, y + h * 0.62),
                (x + w * 0.55, y),
                (x, y - h * 0.62),
                (x - w * 0.55, y)
            ]
            poly = Polygon(verts, closed=True, facecolor="white", edgecolor="black", lw=1.5, zorder=3)
            self.ax.add_patch(poly)
        else:  # Standard process box
            patch = FancyBboxPatch((x - w/2.0, y - h/2.0), w, h,
                                   boxstyle="round,pad=0.06,rounding_size=0.08",
                                   facecolor="white", edgecolor="black", lw=1.5, zorder=3)
            self.ax.add_patch(patch)

        # Draw minimalist black outline icon if assigned
        has_icon = node.icon is not None
        icon_x = x - w/2.0 + 0.38 if node.shape_type != "diamond" else x - w/2.0 + 0.48
        text_x = x + 0.16 if has_icon else x

        if node.icon == "drone":
            draw_drone_icon(self.ax, icon_x, y, size=0.20)
        elif node.icon == "sensor":
            draw_sensor_icon(self.ax, icon_x, y, size=0.18)
        elif node.icon == "decision":
            draw_decision_icon(self.ax, icon_x, y, size=0.18)
        elif node.icon == "sheaf":
            draw_sheaf_core_icon(self.ax, icon_x, y, size=0.20)
        elif node.icon == "target":
            draw_target_icon(self.ax, icon_x, y, size=0.18)
        elif node.icon == "shield":
            draw_shield_icon(self.ax, icon_x, y, size=0.18)
        elif node.icon == "jammer":
            draw_jammer_tower_icon(self.ax, icon_x, y, size=0.18)

        # Draw pure black text
        if node.subtitle:
            self.ax.text(text_x, y + 0.12, node.text, fontsize=9.0, fontweight="bold", 
                         color="black", ha="center", va="center", zorder=5)
            self.ax.text(text_x, y - 0.16, node.subtitle, fontsize=7.8, 
                         color="black", ha="center", va="center", zorder=5)
        else:
            self.ax.text(text_x, y, node.text, fontsize=9.0, fontweight="bold", 
                         color="black", ha="center", va="center", zorder=5)

    def draw_connections(self):
        for conn in self.connections:
            n1 = self.nodes[conn["from"]]
            n2 = self.nodes[conn["to"]]

            fp = conn.get("from_port")
            tp = conn.get("to_port")
            if not fp or not tp:
                auto_fp, auto_tp = self._auto_ports(n1, n2)
                fp = fp or auto_fp
                tp = tp or auto_tp

            start_pt = n1.get_port(fp)
            end_pt = n2.get_port(tp)

            if conn.get("waypoints"):
                pts = [start_pt] + conn["waypoints"] + [end_pt]
                for i in range(len(pts) - 2):
                    self.ax.plot([pts[i][0], pts[i+1][0]], [pts[i][1], pts[i+1][1]],
                                 color="black", lw=1.5, zorder=4)
                self.ax.annotate(
                    "", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(facecolor="black", edgecolor="black", width=1.5,
                                    headwidth=6.0, headlength=6.5, shrink=0.005),
                    zorder=4
                )
                mid_x = (pts[0][0] + pts[-1][0]) / 2.0
                mid_y = (pts[0][1] + pts[-1][1]) / 2.0
            else:
                self.ax.annotate(
                    "", xy=end_pt, xytext=start_pt,
                    arrowprops=dict(facecolor="black", edgecolor="black", width=1.5,
                                    headwidth=6.0, headlength=6.5, shrink=0.005),
                    zorder=4
                )
                mid_x = (start_pt[0] + end_pt[0]) / 2.0
                mid_y = (start_pt[1] + end_pt[1]) / 2.0

            if conn.get("label"):
                lx = mid_x + conn["label_offset"][0]
                ly = mid_y + conn["label_offset"][1]
                self.ax.text(lx, ly, conn["label"], fontsize=8.0, fontweight="bold",
                             color="black", ha="center", va="center",
                             bbox=dict(boxstyle="square,pad=0.2", facecolor="white", edgecolor="black", lw=0.8),
                             zorder=6)

    def render(self, output_path):
        if self.title:
            title_box = FancyBboxPatch((0.5, self.height - 0.75), self.width - 1.0, 0.55,
                                       boxstyle="square,pad=0.05",
                                       facecolor="white", edgecolor="black", lw=1.5, zorder=3)
            self.ax.add_patch(title_box)
            self.ax.text(self.width / 2.0, self.height - 0.48, self.title, 
                         color="black", fontsize=10.5, fontweight="bold", ha="center", va="center", zorder=5)

        # Draw connections first so nodes sit cleanly above any lines if slightly close
        self.draw_connections()

        for node in self.nodes.values():
            self.draw_shape(node)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Flowchart successfully saved to {output_path}")
