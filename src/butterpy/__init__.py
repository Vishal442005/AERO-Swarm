"""
butterpy: Simple, publication-grade flowchart generation extension for Python.
"""

from .flowchart import ButterFlowchart
from .icons import (
    draw_drone_icon, draw_sensor_icon, draw_decision_icon,
    draw_sheaf_core_icon, draw_target_icon, draw_shield_icon, draw_jamming_tower_icon
)

__version__ = "1.0.0"
__all__ = ["ButterFlowchart"]
