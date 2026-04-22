"""
visualization.py: Animation and Force Visualization

Provides visualization tools for:
- Linkage mechanism animation
- Force vector diagrams
- Stress distribution plots
- Phase diagrams and performance maps
"""

import numpy as np
from typing import Dict, Optional
import math


def configure_fonts():
    """
    Configure matplotlib to use Chinese fonts if available.
    """
    try:
        import matplotlib.pyplot as plt
        import matplotlib.font_manager as fm
        
        # Common Chinese fonts for Windows and Linux
        chinese_fonts = ['SimHei', 'Microsoft YaHei', 'Noto Sans SC', 'STHeiti', 'DejaVu Sans']
        
        available_fonts = [f.name for f in fm.fontManager.ttflist]
        font_to_use = [f for f in chinese_fonts if f in available_fonts]
        
        if font_to_use:
            plt.rcParams['font.sans-serif'] = font_to_use
            plt.rcParams['axes.unicode_minus'] = False
    except ImportError:
        pass


class Visualizer:
    """
    Visualization tools for four-bar linkage analysis.
    """
    
    def __init__(self, linkage=None):
        """
        Initialize visualizer.
        
        Args:
            linkage: FourBarLinkage instance (optional)
        """
        self.linkage = linkage
        self.figure = None
        self.axes = None
        configure_fonts()
    
    def plot_linkage_configuration(self, show_forces: bool = False, 
                                   force_dict: Dict = None):
        """
        Plot current linkage configuration.
        
        Args:
            show_forces: Whether to show force vectors
            force_dict: Dictionary of forces at each joint
        """
        import matplotlib.pyplot as plt
        
        if self.linkage is None or self.linkage.C is None:
            raise ValueError("Linkage must be configured first")
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        positions = self.linkage.get_joint_positions()
        
        # Extract coordinates
        A, B, C, D = positions['A'], positions['B'], positions['C'], positions['D']
        
        # Plot links as lines
        links = [
            (A, C, 'input crank'),
            (C, D, 'coupler'),
            (D, B, 'output link'),
            (B, A, 'base frame')
        ]
        
        for start, end, label in links:
            ax.plot([start[0], end[0]], [start[1], end[1]], 'b-', linewidth=2)
            mid = (start + end) / 2
            ax.text(mid[0], mid[1], label, fontsize=9, ha='center')
        
        # Plot joints
        joint_dict = {'A': A, 'B': B, 'C': C, 'D': D}
        for name, pos in joint_dict.items():
            if name in ['A', 'B']:
                ax.plot(pos[0], pos[1], 'ro', markersize=10, label=f'{name} (pivot)')
            else:
                ax.plot(pos[0], pos[1], 'go', markersize=8, label=f'{name}')
            ax.text(pos[0], pos[1]+50, name, fontsize=12, fontweight='bold')
        
        # Plot forces if provided
        if show_forces and force_dict:
            force_scale = 0.01  # Scale for visualization
            for joint, force in force_dict.items():
                if joint in joint_dict and isinstance(force, np.ndarray):
                    pos = joint_dict[joint]
                    ax.arrow(pos[0], pos[1], 
                            force[0]*force_scale, force[1]*force_scale,
                            head_width=30, head_length=20, fc='red', ec='red')
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X (mm)')
        ax.set_ylabel('Y (mm)')
        ax.set_title('Four-Bar Linkage Configuration')
        ax.legend(loc='best', fontsize=9)
        
        return fig, ax
    
    def plot_mechanism_workspace(self, input_angle_range: tuple = (0, 2*math.pi),
                                n_points: int = 50):
        """
        Plot the workspace of the output joint.
        
        Args:
            input_angle_range: Tuple of (min_angle, max_angle) in radians
            n_points: Number of points to calculate
        """
        import matplotlib.pyplot as plt
        
        if self.linkage is None:
            raise ValueError("Linkage must be provided")
        
        angles = np.linspace(input_angle_range[0], input_angle_range[1], n_points)
        positions = []
        
        for angle in angles:
            try:
                self.linkage.forward_kinematics(angle)
                D = self.linkage.D
                positions.append((D[0], D[1], angle))
            except ValueError:
                continue  # Skip impossible configurations
        
        if not positions:
            print("No valid configurations found")
            return None, None
        
        positions = np.array(positions)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Color by input angle
        scatter = ax.scatter(positions[:, 0], positions[:, 1], 
                           c=positions[:, 2], cmap='hsv', s=50, alpha=0.6)
        
        ax.plot([self.linkage.B[0]], [self.linkage.B[1]], 'ko', 
               markersize=10, label='Base pivot B')
        
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('X (mm)')
        ax.set_ylabel('Y (mm)')
        ax.set_title('Output Joint Workspace')
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Input Angle (rad)')
        ax.legend()
        
        return fig, ax
    
    def plot_force_profile(self, simulation_history: Dict):
        """
        Plot force profiles over time from simulation.
        
        Args:
            simulation_history: Dictionary from DynamicSimulation.history
        """
        import matplotlib.pyplot as plt
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        times = simulation_history.get('times', [])
        
        # Plot 1: Coal and Hydraulic Forces
        ax = axes[0, 0]
        ax.plot(times, simulation_history.get('coal_forces', []), 'b-', label='Coal Force')
        ax.plot(times, simulation_history.get('hydraulic_forces', []), 'r-', label='Hydraulic Force')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Force (N)')
        ax.set_title('Forces vs Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 2: Bearing Loads at A and B
        ax = axes[0, 1]
        bearing_loads = simulation_history.get('bearing_loads', {})
        if 'A' in bearing_loads:
            ax.plot(times, bearing_loads['A'], label='Joint A')
        if 'B' in bearing_loads:
            ax.plot(times, bearing_loads['B'], label='Joint B')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Bearing Load (N)')
        ax.set_title('Bearing Loads vs Time')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 3: Input and Output Angles
        ax = axes[1, 0]
        ax.plot(times, np.degrees(simulation_history.get('input_angles', [])), 'g-')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Input Angle (degrees)')
        ax.set_title('Input Angle vs Time')
        ax.grid(True, alpha=0.3)
        
        # Plot 4: Output Velocity
        ax = axes[1, 1]
        ax.plot(times, simulation_history.get('output_velocities', []), 'm-')
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Output Velocity (m/s)')
        ax.set_title('Output Velocity vs Time')
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        return fig, axes
    
    def plot_mechanical_advantage_map(self, input_angle_range: tuple = (0, math.pi),
                                     n_points: int = 30):
        """
        Plot mechanical advantage across input angle range.
        
        Args:
            input_angle_range: Tuple of (min_angle, max_angle)
            n_points: Number of evaluation points
        """
        import matplotlib.pyplot as plt
        from .forces import ForceAnalysis
        
        if self.linkage is None:
            raise ValueError("Linkage must be provided")
        
        analyzer = ForceAnalysis(self.linkage)
        
        angles = np.linspace(input_angle_range[0], input_angle_range[1], n_points)
        advantages = []
        
        for angle in angles:
            try:
                advantage = analyzer.calculate_mechanical_advantage(angle)
                advantages.append(advantage)
            except ValueError:
                advantages.append(np.nan)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(np.degrees(angles), advantages, 'b-', linewidth=2)
        ax.set_xlabel('Input Crank Angle (degrees)')
        ax.set_ylabel('Mechanical Advantage')
        ax.set_title('Mechanical Advantage vs Input Angle')
        ax.grid(True, alpha=0.3)
        
        return fig, ax
    
    @staticmethod
    def save_figure(fig, filename: str):
        """Save figure to file."""
        fig.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Figure saved to {filename}")


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from .structure import FourBarLinkage, FourBarDimensions
    
    dims = FourBarDimensions(
        base_length=1000,
        input_crank=250,
        coupler=800,
        output_link=600
    )
    
    linkage = FourBarLinkage(dims)
    linkage.forward_kinematics(math.radians(45))
    
    visualizer = Visualizer(linkage)
    fig, ax = visualizer.plot_linkage_configuration()
    plt.show()
