"""
simulation.py: Dynamic Simulation Engine

Simulates the dynamic behavior of the four-bar hydraulic support system including:
- Time-domain kinematic simulation
- Velocity and acceleration calculations
- Energy absorption during coal loading
- Fatigue analysis
"""

import numpy as np
from typing import Dict, List, Tuple
import math
from .structure import FourBarLinkage, FourBarDimensions
from .forces import ForceAnalysis


class DynamicSimulation:
    """
    Dynamic simulation of four-bar hydraulic support under coal loading.
    """
    
    def __init__(self, linkage: FourBarLinkage, mass_properties: Dict = None):
        """
        Initialize dynamic simulator.
        
        Args:
            linkage: FourBarLinkage instance
            mass_properties: Dictionary with 'crank', 'coupler', 'output' masses (kg)
        """
        self.linkage = linkage
        self.force_analyzer = ForceAnalysis(linkage)
        
        # Default mass properties (kg)
        self.mass = mass_properties or {
            'crank': 15,
            'coupler': 45,
            'output': 35
        }
        
        # Hydraulic properties
        self.hydraulic_flow_rate = 1e-4  # m³/s (100 cc/min)
        self.cylinder_bore = 63e-3       # 63 mm bore (common for coal supports)
        self.cylinder_rod = 40e-3        # 40 mm rod
        self.pump_pressure = 25e6        # 25 MPa (250 bar)
        
        # Damping
        self.damping_ratio = 0.3  # 30% critical damping
        
        # Simulation history
        self.history = {}
    
    def run_simulation(self, 
                      duration: float,
                      dt: float = 0.01,
                      coal_force_profile: callable = None) -> Dict:
        """
        Run time-domain simulation.
        
        Args:
            duration: Total simulation time (seconds)
            dt: Time step (seconds)
            coal_force_profile: Function f(t) returning coal force at time t
                              Default: constant 50 kN
            
        Returns:
            Dictionary containing simulation results
        """
        if coal_force_profile is None:
            coal_force_profile = lambda t: 50000  # 50 kN constant
        
        # Initialize arrays
        times = np.arange(0, duration, dt)
        n_steps = len(times)
        
        # State: [input_angle, input_velocity, output_velocity, ...]
        input_angles = np.zeros(n_steps)
        input_velocities = np.zeros(n_steps)
        output_positions = [None] * n_steps
        output_velocities = np.zeros(n_steps)
        coal_forces = np.zeros(n_steps)
        hydraulic_forces = np.zeros(n_steps)
        bearing_loads = {joint: np.zeros(n_steps) 
                        for joint in ['A', 'B', 'C', 'D']}
        
        # Initial condition
        input_angles[0] = math.radians(10)  # Start at 10°
        input_velocities[0] = 0.0
        
        # Time stepping
        for i in range(1, n_steps):
            t = times[i]
            theta = input_angles[i-1]
            omega = input_velocities[i-1]
            
            # Forward kinematics
            self.linkage.forward_kinematics(theta)
            C, D = self.linkage.C, self.linkage.D
            output_positions[i] = D.copy()
            
            # Get coal force at this time
            F_coal = coal_force_profile(t)
            coal_forces[i] = F_coal
            
            # Force analysis
            analysis = self.force_analyzer.analyze_static_forces(F_coal)
            hydraulic_forces[i] = analysis['hydraulic_force']
            
            # Store bearing loads
            for joint in ['A', 'B', 'C', 'D']:
                bearing_loads[joint][i] = analysis['bearing_loads'][joint]
            
            # Calculate derivatives (kinematic)
            theta_dot = self._calculate_input_velocity(theta)
            d_omega_dt = self._calculate_acceleration(
                theta, omega, F_coal, hydraulic_forces[i]
            )
            
            # Update state (simple Euler method)
            input_angles[i] = theta + omega * dt
            input_velocities[i] = omega + d_omega_dt * dt
            
            # Output velocity (numerical derivative)
            if output_positions[i-1] is not None:
                output_vel = (np.linalg.norm(output_positions[i] - output_positions[i-1]) / dt)
                output_velocities[i] = output_vel
        
        # Store results
        self.history = {
            'times': times,
            'input_angles': input_angles,
            'input_velocities': input_velocities,
            'output_positions': output_positions,
            'output_velocities': output_velocities,
            'coal_forces': coal_forces,
            'hydraulic_forces': hydraulic_forces,
            'bearing_loads': bearing_loads
        }
        
        return self._summarize_results(times, coal_forces, hydraulic_forces, 
                                      bearing_loads, output_velocities)
    
    def _calculate_input_velocity(self, theta: float) -> float:
        """Calculate input velocity based on hydraulic cylinder speed."""
        # Velocity of hydraulic piston
        piston_area = math.pi * (self.cylinder_bore / 2) ** 2
        piston_velocity = self.hydraulic_flow_rate / piston_area
        
        # Convert to input angle velocity
        crank_length = self.linkage.dimensions.input_crank
        omega = piston_velocity / crank_length if crank_length > 0 else 0
        
        return omega
    
    def _calculate_acceleration(self, theta: float, omega: float,
                               coal_force: float, hydraulic_force: float) -> float:
        """Calculate angular acceleration using energy method."""
        
        # Effective moment of inertia at input crank
        I_crank = self.mass['crank'] * (self.linkage.dimensions.input_crank ** 2) / 3
        
        # Motor torque from hydraulic pressure
        piston_area = math.pi * (self.cylinder_bore / 2) ** 2
        torque_motor = hydraulic_force * self.linkage.dimensions.input_crank
        
        # Resistance torque from coal load (simplified)
        torque_coal = coal_force * self.linkage.dimensions.output_link * 0.5
        
        # Damping torque (proportional to velocity)
        c_damping = 2 * self.damping_ratio * math.sqrt(I_crank)
        torque_damping = c_damping * omega
        
        # Net torque and acceleration
        torque_net = torque_motor - torque_coal - torque_damping
        alpha = torque_net / (I_crank + 1e-6)
        
        return alpha
    
    def _summarize_results(self, times, coal_forces, hydraulic_forces, 
                         bearing_loads, output_velocities) -> Dict:
        """Create summary statistics from simulation."""
        
        return {
            'duration': times[-1] if len(times) > 0 else 0,
            'max_coal_force': float(np.max(coal_forces)) if len(coal_forces) > 0 else 0,
            'avg_coal_force': float(np.mean(coal_forces)) if len(coal_forces) > 0 else 0,
            'max_hydraulic_force': float(np.max(hydraulic_forces)) if len(hydraulic_forces) > 0 else 0,
            'avg_hydraulic_force': float(np.mean(hydraulic_forces)) if len(hydraulic_forces) > 0 else 0,
            'max_bearing_load_A': float(np.max(bearing_loads['A'])) if 'A' in bearing_loads else 0,
            'max_bearing_load_B': float(np.max(bearing_loads['B'])) if 'B' in bearing_loads else 0,
            'max_output_velocity': float(np.max(output_velocities)) if len(output_velocities) > 0 else 0,
            'mean_mechanical_efficiency': float(np.mean([
                coal_forces[i] / (hydraulic_forces[i] + 1e-6)
                for i in range(len(times)) if hydraulic_forces[i] > 0
            ]))
        }
    
    def get_fatigue_estimate(self, stress_concentration_factor: float = 1.5) -> Dict:
        """
        Estimate fatigue life using Miner's rule.
        
        Args:
            stress_concentration_factor: Kt for stress concentration
            
        Returns:
            Estimated fatigue life in cycles
        """
        if not self.history:
            raise ValueError("Must run simulation first")
        
        bearing_loads = self.history['bearing_loads']
        
        # S-N curve for structural steel (simplified, R=-1)
        # Fatigue strength at 10^6 cycles ≈ 0.4 * yield
        steel_fatigue_strength = 0.4 * 350e6
        
        # Estimate cycles to failure (Miner's rule)
        cycles_estimate = {}
        for joint in bearing_loads:
            max_stress = bearing_loads[joint].max() * stress_concentration_factor
            if max_stress > 0:
                # Simplified Wöhler curve
                cycles = (steel_fatigue_strength / max_stress) ** 8
                cycles_estimate[f'{joint}_cycles'] = int(cycles)
        
        return cycles_estimate


if __name__ == "__main__":
    dims = FourBarDimensions(
        base_length=1000,
        input_crank=250,
        coupler=800,
        output_link=600
    )
    
    linkage = FourBarLinkage(dims)
    simulator = DynamicSimulation(linkage)
    
    # Run 1 second simulation with 50 kN constant coal force
    results = simulator.run_simulation(
        duration=1.0,
        dt=0.01,
        coal_force_profile=lambda t: 50000
    )
    
    print("Simulation Results:")
    for key, value in results.items():
        print(f"  {key}: {value}")
    
    # Fatigue estimate
    fatigue = simulator.get_fatigue_estimate()
    print("\nFatigue Life Estimates:")
    for key, value in fatigue.items():
        print(f"  {key}: {value:.0e} cycles")
