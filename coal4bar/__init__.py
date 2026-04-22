"""
coal4bar: Four-Bar Hydraulic Support Simulation and Analysis Tool

A comprehensive simulation engine for four-bar linkage hydraulic supports used in coal mining.
This module provides tools for:
- Structural geometry and kinematics analysis
- Force and stress distribution calculation
- Dynamic simulation of support behavior
- Visual analysis and optimization
- Safety coefficient determination
"""

__version__ = "0.1.0"
__author__ = "coal4bar development team"

from .structure import FourBarLinkage
from .forces import ForceAnalysis
from .simulation import DynamicSimulation
from .visualization import Visualizer
from .safety_analysis import SafetyAnalyzer

__all__ = [
    'FourBarLinkage',
    'ForceAnalysis',
    'DynamicSimulation',
    'Visualizer',
    'SafetyAnalyzer',
]
