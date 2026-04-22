"""Example 2: Dynamic Simulation of Coal Loading Scenario"""

import math
import sys
sys.path.insert(0, '..')

from coal4bar import FourBarLinkage, DynamicSimulation, Visualizer
from coal4bar.structure import FourBarDimensions


def example_dynamic_simulation():
    """Run a dynamic simulation with time-varying coal load."""
    
    print("=" * 70)
    print("EXAMPLE 2: Dynamic Simulation with Coal Loading")
    print("=" * 70)
    
    # Create linkage
    dimensions = FourBarDimensions(
        base_length=1000,
        input_crank=250,
        coupler=800,
        output_link=600
    )
    
    linkage = FourBarLinkage(dimensions)
    
    # Create simulator with mass properties
    mass_props = {
        'crank': 15,        # kg
        'coupler': 45,      # kg
        'output': 35        # kg
    }
    
    simulator = DynamicSimulation(linkage, mass_properties=mass_props)
    
    # Define a coal loading profile
    # Simulate loading sequence: ramp up, hold, ramp down
    def coal_force_profile(t):
        """Coal loading profile as function of time."""
        if t < 0.5:
            # Ramp up to 50 kN over 0.5 seconds
            return 50000 * (t / 0.5)
        elif t < 1.5:
            # Hold at 50 kN
            return 50000
        elif t < 2.0:
            # Ramp down
            return 50000 * (2.0 - t) / 0.5
        else:
            # Unloaded
            return 5000
    
    print("\n1. Simulation Configuration:")
    print(f"   Hydraulic flow rate: {simulator.hydraulic_flow_rate*1e6:.0f} cc/min")
    print(f"   Cylinder bore: {simulator.cylinder_bore*1000:.1f} mm")
    print(f"   System pressure: {simulator.pump_pressure/1e6:.0f} MPa")
    print(f"   Damping ratio: {simulator.damping_ratio:.1%}")
    
    # Run simulation
    print("\n2. Running 2-second simulation...")
    results = simulator.run_simulation(
        duration=2.0,
        dt=0.01,
        coal_force_profile=coal_force_profile
    )
    
    print("\n3. Simulation Results Summary:")
    print(f"   Duration: {results['duration']:.2f} seconds")
    print(f"   Max coal force: {results['max_coal_force'] / 1000:.1f} kN")
    print(f"   Average coal force: {results['avg_coal_force'] / 1000:.1f} kN")
    print(f"   Max hydraulic force: {results['max_hydraulic_force'] / 1000:.1f} kN")
    print(f"   Max bearing load (A): {results['max_bearing_load_A']:.0f} N")
    print(f"   Max bearing load (B): {results['max_bearing_load_B']:.0f} N")
    print(f"   Max output velocity: {results['max_output_velocity']:.4f} m/s")
    print(f"   Mean mechanical efficiency: {results['mean_mechanical_efficiency']:.3f}")
    
    # Fatigue estimate
    print("\n4. Fatigue Life Estimate (at max stress):")
    fatigue = simulator.get_fatigue_estimate(stress_concentration_factor=1.3)
    for key, value in fatigue.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.2e} cycles")
    
    # Generate plots (if matplotlib available)
    try:
        import matplotlib.pyplot as plt
        
        visualizer = Visualizer(linkage)
        fig, axes = visualizer.plot_force_profile(simulator.history)
        
        # Save the plot
        plt.savefig('simulation_results.png', dpi=100, bbox_inches='tight')
        print("\n5. Plots saved to 'simulation_results.png'")
        
    except ImportError:
        print("\n5. Matplotlib not available for plotting")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    example_dynamic_simulation()
