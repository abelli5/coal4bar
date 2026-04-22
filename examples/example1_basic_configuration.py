"""Example 1: Basic Four-Bar Linkage Configuration and Analysis"""

import math
import sys
sys.path.insert(0, '..')

from coal4bar import FourBarLinkage, ForceAnalysis, SafetyAnalyzer
from coal4bar.structure import FourBarDimensions


def example_basic_configuration():
    """Create and analyze a basic four-bar hydraulic support."""
    
    print("=" * 70)
    print("EXAMPLE 1: Basic Four-Bar Linkage Configuration")
    print("=" * 70)
    
    # Define linkage dimensions (typical coal support)
    # All dimensions in millimeters
    dimensions = FourBarDimensions(
        base_length=1000,      # Fixed frame width
        input_crank=250,       # Hydraulic cylinder crank
        coupler=800,           # Intermediate link
        output_link=600        # Support leg
    )
    
    # Validate Grashof criterion
    print("\n1. Linkage Design:")
    print(f"   Base frame (L0):   {dimensions.base_length} mm")
    print(f"   Input crank (L1):  {dimensions.input_crank} mm")
    print(f"   Coupler (L2):      {dimensions.coupler} mm")
    print(f"   Output link (L3):  {dimensions.output_link} mm")
    print(f"   Is Grashof compatible: {dimensions.validate_grashof_criterion()}")
    
    # Create linkage
    linkage = FourBarLinkage(dimensions)
    
    # Analyze at several input angles
    print("\n2. Kinematic Analysis (Forward Kinematics):")
    print("   Input Angle | Output Angle | C Position      | D Position")
    print("   " + "-" * 65)
    
    input_angles_deg = [0, 30, 60, 90, 120, 150]
    
    for angle_deg in input_angles_deg:
        angle_rad = math.radians(angle_deg)
        
        try:
            C, D = linkage.forward_kinematics(angle_rad)
            output_angle_deg = math.degrees(linkage.get_output_angle())
            
            print(f"   {angle_deg:3d}°      | {output_angle_deg:7.2f}°      | "
                  f"({C[0]:7.1f}, {C[1]:7.1f}) | ({D[0]:7.1f}, {D[1]:7.1f})")
        except ValueError as e:
            print(f"   {angle_deg:3d}°      | INVALID CONFIG  | {str(e)}")
    
    # Force analysis at 45 degrees
    print("\n3. Force Analysis (at 45° input angle):")
    linkage.forward_kinematics(math.radians(45))
    analyzer = ForceAnalysis(linkage)
    
    coal_force = 50000  # 50 kN
    forces = analyzer.analyze_static_forces(coal_force=coal_force)
    
    print(f"   Coal compression force: {coal_force / 1000:.1f} kN")
    print(f"   Required hydraulic force: {forces['hydraulic_force'] / 1000:.2f} kN")
    print(f"   Mechanical advantage: {forces['mechanical_advantage']:.3f}")
    
    print("\n   Bearing loads (N):")
    for joint in ['A', 'B', 'C', 'D']:
        load = forces['bearing_loads'][joint]
        print(f"      Joint {joint}: {load:.1f} N")
    
    # Safety analysis
    print("\n4. Safety Analysis:")
    safety_analyzer = SafetyAnalyzer(linkage)
    stability = safety_analyzer.analyze_linkage_stability()
    
    print(f"   Mechanism type: {stability['linkage_type']}")
    print(f"   Has dead centers: {stability['has_dead_center']}")
    print(f"   Aspect ratio: {stability['aspect_ratios']['aspect_ratio']:.3f}")
    
    # Bearing safety
    max_bearing_load = max(forces['bearing_loads'].values())
    bearing_safety = safety_analyzer.analyze_bearing_loads(max_bearing_load)
    
    print(f"\n   Bearing safety (max load {max_bearing_load:.0f} N):")
    print(f"      Contact stress: {bearing_safety['contact_pressure']:.2e} Pa")
    print(f"      Safety factor: {bearing_safety['safety_factor_bearing']:.2f}")
    print(f"      L10 life: {bearing_safety['L10_life_hours']:.0f} hours")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    example_basic_configuration()
