"""
structure.py: Four-Bar Linkage Geometry and Kinematics

Handles the geometric modeling and kinematic analysis of the four-bar linkage system.
A four-bar linkage consists of:
- Fixed frame (base)
- Input crank (connected to hydraulic cylinder)
- Coupler (intermediate link)
- Output link (supports coal seam)
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict
import math


@dataclass
class Link:
    """Represents a single link in the four-bar mechanism."""
    length: float
    name: str
    
    def validate(self):
        """Ensure link length is positive."""
        if self.length <= 0:
            raise ValueError(f"Link length must be positive: {self.length}")


@dataclass
class FourBarDimensions:
    """Dimensions of the four-bar linkage."""
    base_length: float      # L0: Fixed base frame
    input_crank: float      # L1: Input crank (connected to hydraulic cylinder)
    coupler: float          # L2: Coupler link
    output_link: float      # L3: Output link (supports coal seam)
    
    def validate_grashof_criterion(self) -> bool:
        """
        Validate Grashof's criterion for continuous rotation.
        For a four-bar linkage to have continuous rotation:
        s + l < p + q
        where s is shortest link, l is longest link, p and q are intermediate links.
        """
        lengths = [self.base_length, self.input_crank, self.coupler, self.output_link]
        s = min(lengths)
        l = max(lengths)
        p, q = sorted([x for x in lengths if x != s and x != l])
        
        return s + l <= p + q
    
    def get_links(self) -> Tuple[float, float, float, float]:
        """Return all link lengths."""
        return (self.base_length, self.input_crank, 
                self.coupler, self.output_link)


class FourBarLinkage:
    """
    Four-bar hydraulic support linkage model.
    
    Coordinate system:
    - Origin at the base pivot (fixed frame start)
    - X-axis along the base frame
    - Y-axis perpendicular to base frame
    """
    
    def __init__(self, dimensions: FourBarDimensions):
        """
        Initialize the four-bar linkage.
        
        Args:
            dimensions: FourBarDimensions containing all link lengths
        """
        self.dimensions = dimensions
        self.dimensions.validate_grashof_criterion()
        
        # Joint positions
        self.A = np.array([0.0, 0.0])              # Fixed pivot 1
        self.B = np.array([dimensions.base_length, 0.0])  # Fixed pivot 2
        self.C = None  # Input joint (varies with input angle)
        self.D = None  # Output joint (calculated from linkage)
    
    def forward_kinematics(self, input_angle: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate joint positions given input crank angle.
        
        Args:
            input_angle: Input crank angle (radians) measured from base frame
            
        Returns:
            (C_position, D_position): Positions of intermediate and output joints
        """
        # Position of C (end of input crank)
        C = self.A + self.dimensions.input_crank * np.array([
            math.cos(input_angle),
            math.sin(input_angle)
        ])
        
        # Find D position: solve two-circle intersection
        # Circle 1: centered at C with radius = coupler length
        # Circle 2: centered at B with radius = output link length
        D = self._solve_linkage_position(C)
        
        self.C = C
        self.D = D
        
        return C, D
    
    def _solve_linkage_position(self, C: np.ndarray) -> np.ndarray:
        """
        Solve for output joint D position using two-circle intersection.
        
        Circle 1 (coupler): ||D - C|| = L2
        Circle 2 (output):   ||D - B|| = L3
        """
        # Distance from C to intermediate point
        d = np.linalg.norm(self.B - C)
        
        # Check if solution exists
        L2, L3 = self.dimensions.coupler, self.dimensions.output_link
        if d > L2 + L3 or d < abs(L2 - L3):
            raise ValueError(f"Linkage configuration impossible: d={d}, L2={L2}, L3={L3}")
        
        # Calculate intersection point
        a = (d**2 + L2**2 - L3**2) / (2 * d)
        h = math.sqrt(max(0, L2**2 - a**2))
        
        # Intermediate point on line CB
        P = C + a * (self.B - C) / d
        
        # Perpendicular direction (take upper solution)
        perp = np.array([-(self.B[1] - C[1]), self.B[0] - C[0]]) / d
        
        # Solution with positive y-component (upper branch)
        D = P + h * perp
        
        return D
    
    def get_output_angle(self) -> float:
        """
        Calculate output link angle with respect to base frame.
        
        Returns:
            Output link angle in radians
        """
        if self.D is None:
            raise ValueError("Must call forward_kinematics first")
        
        output_vector = self.D - self.B
        return math.atan2(output_vector[1], output_vector[0])
    
    def get_joint_positions(self) -> Dict[str, np.ndarray]:
        """Return positions of all joints."""
        if self.C is None or self.D is None:
            raise ValueError("Must call forward_kinematics first")
        
        return {
            'A': self.A.copy(),
            'B': self.B.copy(),
            'C': self.C.copy(),
            'D': self.D.copy()
        }
    
    def get_link_lengths(self) -> Dict[str, float]:
        """Return current link lengths (should be constant)."""
        positions = self.get_joint_positions()
        return {
            'AB': np.linalg.norm(positions['B'] - positions['A']),
            'AC': np.linalg.norm(positions['C'] - positions['A']),
            'CD': np.linalg.norm(positions['D'] - positions['C']),
            'BD': np.linalg.norm(positions['D'] - positions['B']),
        }


if __name__ == "__main__":
    # Example: Create and test four-bar linkage
    dims = FourBarDimensions(
        base_length=1000,      # 1000 mm
        input_crank=250,       # 250 mm
        coupler=800,           # 800 mm
        output_link=600        # 600 mm
    )
    
    linkage = FourBarLinkage(dims)
    
    # Test at several input angles
    for angle_deg in [0, 30, 60, 90]:
        angle_rad = math.radians(angle_deg)
        C, D = linkage.forward_kinematics(angle_rad)
        print(f"Input: {angle_deg}° => C={C}, D={D}")
        print(f"Output angle: {math.degrees(linkage.get_output_angle()):.2f}°\n")
