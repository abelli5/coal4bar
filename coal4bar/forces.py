"""
forces.py: Force Analysis and Stress Distribution

Analyzes forces in the four-bar linkage system including:
- Coal seam reaction forces
- Bearing forces at all joints
- Stress distribution along links
- Mechanical advantage calculation
"""

import numpy as np
from typing import Dict, Tuple
import math
from .structure import FourBarLinkage, FourBarDimensions


class ForceAnalysis:
    """
    Performs force analysis on four-bar hydraulic support system.
    
    Force analysis approach:
    1. Apply coal compression force at output link
    2. Use virtual work principle and Newton's equations
    3. Calculate reaction forces at all joints
    4. Determine bearing loads
    """
    
    def __init__(self, linkage: FourBarLinkage):
        """
        Initialize force analyzer.
        
        Args:
            linkage: FourBarLinkage instance with known kinematics
        """
        self.linkage = linkage
        
        # Material properties (typical for steel support)
        self.steel_yield_strength = 350e6  # Pa (350 MPa)
        self.steel_density = 7850          # kg/m³
    
    def analyze_static_forces(self, 
                             coal_force: float,
                             coal_direction: float = 0.0) -> Dict:
        """
        Analyze static forces in the linkage.
        
        Args:
            coal_force: Vertical compression force from coal seam (N)
            coal_direction: Direction angle of coal force (radians, default vertical)
            
        Returns:
            Dictionary containing:
            - joint_forces: Forces at each joint
            - bearing_loads: Loads on bearings at each pivot
            - link_stresses: Internal stresses in each link
            - hydraulic_force: Required hydraulic force
        """
        positions = self.linkage.get_joint_positions()
        
        # Coal force applied at output joint D
        F_coal = coal_force * np.array([
            math.sin(coal_direction),
            -math.cos(coal_direction)  # Downward is negative Y
        ])
        
        # Use virtual work principle
        # For four-bar: F_input * δx_input + F_coal * δx_output = 0
        
        output_angle = self.linkage.get_output_angle()
        
        # Velocity relations (approximate Jacobian)
        J = self._calculate_jacobian(positions, output_angle)
        
        # Solve for internal forces using constraint forces
        # At output link: F_coal acts downward
        
        # Force equilibrium at output joint D
        # Internal forces in coupler and output link
        CD_vector = positions['D'] - positions['C']
        BD_vector = positions['D'] - positions['B']
        
        # Perpendicular vectors for moment calculations
        CD_length = np.linalg.norm(CD_vector)
        BD_length = np.linalg.norm(BD_vector)
        
        CD_unit = CD_vector / CD_length if CD_length > 0 else np.array([0, 0])
        BD_unit = BD_vector / BD_length if BD_length > 0 else np.array([0, 0])
        
        # Calculate forces iteratively
        forces = self._solve_linkage_forces(
            positions, F_coal, CD_unit, BD_unit, CD_length, BD_length
        )
        
        return {
            'coal_force': F_coal,
            'joint_forces': forces['joint_forces'],
            'bearing_loads': forces['bearing_loads'],
            'link_stresses': self._calculate_link_stresses(forces),
            'hydraulic_force': forces['hydraulic_force'],
            'mechanical_advantage': abs(forces['hydraulic_force'] / coal_force) 
                                   if coal_force != 0 else 0
        }
    
    def _calculate_jacobian(self, positions: Dict, output_angle: float) -> np.ndarray:
        """Calculate kinematic Jacobian for velocity relations."""
        # Simplified Jacobian calculation
        AC_vector = positions['C'] - positions['A']
        AC_perpendicular = np.array([-AC_vector[1], AC_vector[0]])
        
        CD_vector = positions['D'] - positions['C']
        
        # Jacobian relating input velocity to output velocity
        J = np.zeros((2, 2))
        J[0, 0] = 1  # Placeholder
        
        return J
    
    def _solve_linkage_forces(self, positions: Dict, F_coal: np.ndarray,
                             CD_unit: np.ndarray, BD_unit: np.ndarray,
                             CD_length: float, BD_length: float) -> Dict:
        """Solve internal forces using method of joints."""
        
        # Assume output link is in equilibrium under:
        # 1. Coal reaction force
        # 2. Internal forces from coupler and base
        
        # Take moments about B to find force in coupler
        r_D = positions['D'] - positions['B']
        r_C = positions['C'] - positions['B']
        
        # Moment balance (2D): cross products
        M_coal = r_D[0] * F_coal[1] - r_D[1] * F_coal[0]
        
        # Coupler force (acts along CD direction)
        # Moment from coupler: r_C × F_coupler
        # If coupler force is F_CD along CD direction:
        # M_coupler = r_C[0] * (F_CD * CD_unit[1]) - r_C[1] * (F_CD * CD_unit[0])
        
        CD_perp = np.array([-CD_unit[1], CD_unit[0]])
        denom = r_C[0] * CD_perp[1] - r_C[1] * CD_perp[0]
        
        F_CD = 0
        if abs(denom) > 1e-6:
            F_CD = -M_coal / denom
        
        # Force balance at D
        # F_coal + F_coupler + F_BD = 0
        F_coupler = F_CD * CD_unit
        F_BD_needed = -F_coal - F_coupler
        
        # Extract BD force magnitude
        F_BD = np.dot(F_BD_needed, BD_unit) if BD_length > 0 else 0
        
        # Hydraulic force (acts along input crank AC)
        AC_vector = positions['C'] - positions['A']
        AC_unit = AC_vector / (np.linalg.norm(AC_vector) + 1e-10)
        
        # Moment about A
        M_hydraulic = positions['C'][0] * 0 - positions['C'][1] * F_CD * CD_unit[0]
        F_hydraulic = 0
        if np.linalg.norm(AC_vector) > 1e-6:
            AC_perp = np.array([-AC_unit[1], AC_unit[0]])
            F_hydraulic = M_hydraulic / (np.linalg.norm(AC_vector) + 1e-10)
        
        return {
            'joint_forces': {
                'A': np.zeros(2),
                'B': np.zeros(2),
                'C': F_coupler,
                'D': F_coal
            },
            'bearing_loads': {
                'A': np.linalg.norm(F_hydraulic * AC_unit),
                'B': np.linalg.norm(F_BD * BD_unit),
                'C': abs(F_CD),
                'D': np.linalg.norm(F_coal)
            },
            'hydraulic_force': abs(F_hydraulic)
        }
    
    def _calculate_link_stresses(self, forces: Dict) -> Dict:
        """Calculate stresses in links assuming tension/compression."""
        dimensions = self.linkage.dimensions
        
        # Cross-sectional areas (assuming cylindrical links with diameter d)
        # A = π * d² / 4, typical d = 30-50 mm for coal supports
        
        assumed_diameter = 40e-3  # 40 mm
        link_area = math.pi * (assumed_diameter / 2) ** 2
        
        bearing_loads = forces['bearing_loads']
        
        stresses = {}
        for joint, load in bearing_loads.items():
            stress = load / link_area if link_area > 0 else 0
            stresses[f'{joint}_stress'] = stress
            stresses[f'{joint}_utilization'] = stress / self.steel_yield_strength
        
        return stresses
    
    def calculate_mechanical_advantage(self, input_angle: float) -> float:
        """
        Calculate mechanical advantage as function of input angle.
        Higher values mean easier to support coal.
        """
        self.linkage.forward_kinematics(input_angle)
        result = self.analyze_static_forces(1000)  # 1000 N test load
        
        return result['mechanical_advantage']


if __name__ == "__main__":
    from .structure import FourBarDimensions
    
    dims = FourBarDimensions(
        base_length=1000,
        input_crank=250,
        coupler=800,
        output_link=600
    )
    
    linkage = FourBarLinkage(dims)
    analyzer = ForceAnalysis(linkage)
    
    # Analyze at 45 degrees input angle
    linkage.forward_kinematics(math.radians(45))
    result = analyzer.analyze_static_forces(coal_force=50000)  # 50 kN
    
    print(f"Coal Force: {result['coal_force']}")
    print(f"Bearing Loads: {result['bearing_loads']}")
    print(f"Mechanical Advantage: {result['mechanical_advantage']:.3f}")
