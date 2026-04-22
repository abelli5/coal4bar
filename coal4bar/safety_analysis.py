"""
safety_analysis.py: Safety Coefficient and Reliability Analysis

Computes safety factors and reliability metrics for the hydraulic support system:
- Material safety factors
- Structural stability analysis
- Energy absorption capacity
- Load path verification
"""

import numpy as np
from typing import Dict
import math


class SafetyAnalyzer:
    """
    Analyzes safety and reliability of four-bar hydraulic support system.
    """
    
    def __init__(self, linkage, material_properties: Dict = None):
        """
        Initialize safety analyzer.
        
        Args:
            linkage: FourBarLinkage instance
            material_properties: Dict with yield_strength, ultimate_strength, etc.
        """
        self.linkage = linkage
        
        # Default material properties (structural steel)
        self.material = material_properties or {
            'name': 'Structural Steel Q345',
            'yield_strength': 345e6,        # Pa
            'ultimate_strength': 520e6,
            'elastic_modulus': 210e9,
            'fatigue_limit': 138e6,         # 0.4 * yield for R=-1
            'density': 7850,
            'poisson_ratio': 0.3
        }
        
        # Design factors (coal mining industry standards)
        self.safety_factor_static = 2.5      # Minimum for static loads
        self.safety_factor_fatigue = 3.0     # Minimum for fatigue
        self.safety_factor_hydraulic = 1.5   # For hydraulic components
    
    def calculate_static_safety_factor(self, max_stress: float) -> float:
        """
        Calculate static safety factor.
        
        Args:
            max_stress: Maximum stress in Pa
            
        Returns:
            Safety factor (yield strength / max stress)
        """
        if max_stress <= 0:
            return float('inf')
        
        sf = self.material['yield_strength'] / max_stress
        return sf
    
    def calculate_fatigue_safety_factor(self, max_stress: float,
                                       min_stress: float = 0,
                                       num_cycles: int = 1000000) -> float:
        """
        Calculate fatigue safety factor using modified Goodman diagram.
        
        Args:
            max_stress: Maximum stress in loading cycle (Pa)
            min_stress: Minimum stress (default 0 = tension only)
            num_cycles: Expected number of cycles
            
        Returns:
            Fatigue safety factor
        """
        sigma_max = max_stress
        sigma_min = min_stress
        sigma_mean = (sigma_max + sigma_min) / 2
        sigma_amplitude = (sigma_max - sigma_min) / 2
        
        # Material fatigue limit (for 10^6 cycles, R=-1)
        S_f_base = self.material['fatigue_limit']
        
        # Adjust for cycle count (Basquin law)
        if num_cycles > 1e6:
            S_f = S_f_base * (1e6 / num_cycles) ** 0.1
        else:
            S_f = S_f_base
        
        # Modified Goodman criterion
        # 1/SF = (sigma_a / S_f) + (sigma_m / S_u) + (sigma_a * sigma_m) / (S_f * S_u)
        
        S_u = self.material['ultimate_strength']
        
        if sigma_amplitude == 0:
            return float('inf')
        
        denominator = (sigma_amplitude / S_f) + (sigma_mean / S_u)
        
        if denominator > 0:
            sf = 1 / denominator
        else:
            sf = float('inf')
        
        return sf
    
    def analyze_linkage_stability(self) -> Dict:
        """
        Analyze structural stability of the linkage.
        
        Returns:
            Dictionary with stability metrics
        """
        dimensions = self.linkage.dimensions
        
        # Check Grashof criterion (for continuous motion)
        is_grashof = dimensions.validate_grashof_criterion()
        
        # Calculate aspect ratios
        longest = max(dimensions.get_links())
        shortest = min(dimensions.get_links())
        
        ratios = {
            'aspect_ratio': longest / shortest if shortest > 0 else 0,
            'base_to_crank': dimensions.base_length / dimensions.input_crank,
            'coupler_to_output': dimensions.coupler / dimensions.output_link
        }
        
        # Stability indicators
        stability = {
            'is_grashof_mechanism': is_grashof,
            'aspect_ratios': ratios,
            'has_dead_center': self._check_dead_centers(),
            'linkage_type': 'Crank-Rocker' if is_grashof else 'Rocker-Rocker'
        }
        
        return stability
    
    def _check_dead_centers(self) -> bool:
        """
        Check if mechanism has dead center positions.
        Dead centers limit the working range.
        """
        L0, L1, L2, L3 = self.linkage.dimensions.get_links()
        
        # Dead center occurs when certain links align
        # Simplified check: if shortest link is too short
        longest = max(L0, L1, L2, L3)
        shortest = min(L0, L1, L2, L3)
        
        return (longest / shortest) > 2.5
    
    def analyze_bearing_loads(self, max_bearing_load: float,
                             bearing_diameter: float = 0.040) -> Dict:
        """
        Analyze bearing safety and life.
        
        Args:
            max_bearing_load: Maximum bearing load (N)
            bearing_diameter: Bearing diameter (m)
            
        Returns:
            Bearing analysis results
        """
        # Contact stress in bearing (Hertzian)
        contact_pressure = self._calculate_hertzian_stress(
            max_bearing_load, bearing_diameter
        )
        
        # Safety factor against bearing failure
        bearing_yield = 1200e6  # Typical bearing steel yield
        sf_bearing = bearing_yield / contact_pressure if contact_pressure > 0 else float('inf')
        
        # Bearing life (ISO 281)
        # L10 = (C / P)^3 * 10^6 cycles (for ball bearings)
        # C = dynamic load rating (function of bearing size)
        c_rating = self._estimate_dynamic_load_rating(bearing_diameter)
        
        if max_bearing_load > 0:
            L10_millions = (c_rating / max_bearing_load) ** 3
            L10_hours = L10_millions * 1e6 / (60 * 500)  # Assume 500 RPM
        else:
            L10_hours = float('inf')
        
        return {
            'contact_pressure': contact_pressure,
            'safety_factor_bearing': sf_bearing,
            'L10_life_hours': L10_hours,
            'dynamic_load_rating': c_rating,
            'acceptable': sf_bearing >= self.safety_factor_static
        }
    
    def _calculate_hertzian_stress(self, load: float, 
                                   diameter: float) -> float:
        """
        Calculate Hertzian contact stress (simplified 2D).
        
        Args:
            load: Load (N)
            diameter: Contact diameter (m)
            
        Returns:
            Contact stress (Pa)
        """
        if diameter <= 0:
            return float('inf')
        
        E = self.material['elastic_modulus']
        v = self.material['poisson_ratio']
        
        # For cylindrical contact, simplified:
        # p_max ≈ sqrt(load * E / (π * diameter * (1-v²)))
        
        contact_stress = math.sqrt(
            load * E / (math.pi * diameter * (1 - v**2))
        )
        
        return contact_stress
    
    def _estimate_dynamic_load_rating(self, bearing_diameter: float) -> float:
        """Estimate dynamic load rating for bearing size."""
        # Empirical: C ≈ 10 * d^2 (for steel bearings, in Newtons)
        return 10 * (bearing_diameter * 1000) ** 2
    
    def analyze_hydraulic_safety(self, max_pressure: float,
                                 system_pressure: float = 25e6) -> Dict:
        """
        Analyze hydraulic system safety.
        
        Args:
            max_pressure: Maximum pressure in system (Pa)
            system_pressure: Operating system pressure (Pa)
            
        Returns:
            Hydraulic safety analysis
        """
        # Pressure relief safety
        relief_setting = system_pressure * 1.1  # 10% above operating
        
        sf_pressure = relief_setting / max_pressure if max_pressure > 0 else float('inf')
        
        # Hose/component ratings (typical coal support equipment)
        rated_pressure = system_pressure * self.safety_factor_hydraulic
        
        results = {
            'max_pressure': max_pressure,
            'system_pressure': system_pressure,
            'relief_setting': relief_setting,
            'safety_factor_pressure': sf_pressure,
            'component_rated_pressure': rated_pressure,
            'acceptable': sf_pressure >= self.safety_factor_hydraulic
        }
        
        return results
    
    def generate_safety_report(self, analysis_results: Dict) -> str:
        """
        Generate comprehensive safety report.
        
        Args:
            analysis_results: Dictionary from complete analysis
            
        Returns:
            Formatted safety report string
        """
        report = ["=" * 60]
        report.append("COAL4BAR - SAFETY ANALYSIS REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Material properties
        report.append("MATERIAL PROPERTIES:")
        for key, value in self.material.items():
            if isinstance(value, float):
                report.append(f"  {key}: {value:.2e} Pa")
            else:
                report.append(f"  {key}: {value}")
        report.append("")
        
        # Linkage stability
        if 'stability' in analysis_results:
            report.append("LINKAGE STABILITY:")
            stability = analysis_results['stability']
            report.append(f"  Grashof Mechanism: {stability['is_grashof_mechanism']}")
            report.append(f"  Type: {stability['linkage_type']}")
            report.append(f"  Aspect Ratio: {stability['aspect_ratios']['aspect_ratio']:.3f}")
            report.append(f"  Dead Centers: {stability['has_dead_center']}")
            report.append("")
        
        # Safety factors
        report.append("SAFETY FACTORS:")
        report.append(f"  Required Static SF: {self.safety_factor_static}")
        report.append(f"  Required Fatigue SF: {self.safety_factor_fatigue}")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


if __name__ == "__main__":
    from .structure import FourBarLinkage, FourBarDimensions
    
    dims = FourBarDimensions(
        base_length=1000,
        input_crank=250,
        coupler=800,
        output_link=600
    )
    
    linkage = FourBarLinkage(dims)
    analyzer = SafetyAnalyzer(linkage)
    
    # Analyze stability
    stability = analyzer.analyze_linkage_stability()
    print("Stability Analysis:")
    print(f"  Is Grashof: {stability['is_grashof_mechanism']}")
    print(f"  Type: {stability['linkage_type']}")
    
    # Bearing analysis
    bearing_analysis = analyzer.analyze_bearing_loads(50000)
    print(f"\nBearing Analysis:")
    print(f"  Contact Pressure: {bearing_analysis['contact_pressure']:.2e} Pa")
    print(f"  Safety Factor: {bearing_analysis['safety_factor_bearing']:.2f}")
    print(f"  L10 Life: {bearing_analysis['L10_life_hours']:.0f} hours")
