"""
coal4bar Project Documentation
==============================

Four-Bar Hydraulic Support Simulation and Analysis Tool
"""

# Physics and Theory

## Four-Bar Linkage Mechanics

A four-bar linkage consists of four rigid links connected by four pivots:

1. **Base frame (L₀)**: Fixed between ground anchors
2. **Input crank (L₁)**: Driven by hydraulic cylinder, rotates about fixed pivot A
3. **Coupler link (L₂)**: Connects the moving pivots C and D
4. **Output link (L₃)**: Supports coal load, rotates about fixed pivot B

### Kinematic Equations

**Forward Kinematics** - Given input angle θ, find output position:

Position of C (crank endpoint):
```
C_x = L₀ + L₁·cos(θ)
C_y = L₁·sin(θ)
```

Position of D (output joint) found by solving:
```
||D - C|| = L₂  (coupler constraint)
||D - B|| = L₃  (output link constraint)
```

This is a two-circle intersection problem solved analytically.

### Grashof Criterion

For continuous single-crank rotation:
```
s + l ≤ p + q
```

Where s = shortest link, l = longest link, p, q = intermediate links.

This determines if the mechanism can perform continuous motion without dead centers.

## Force Analysis

### Static Equilibrium

Given a coal loading force F_coal at joint D, the system must satisfy:

1. **Force balance at each joint**
2. **Moment balance about fixed pivots**

Using virtual work principle or method of joints:

The required hydraulic force F_hyd is calculated from:
- Moment about fixed pivot A
- Geometric advantage (link ratios)
- Current configuration angle

### Mechanical Advantage

```
MA = F_coal / F_hydraulic
```

The mechanical advantage varies with input angle - higher at certain positions 
(better for supporting load) and lower at others.

## Safety Analysis

### Static Safety Factor

```
SF_static = σ_yield / σ_max
```

Required minimum: **2.5** for coal support equipment (industry standard)

### Fatigue Safety Factor

Using modified Goodman criterion with stress amplitude and mean stress:

```
SF_fatigue = 1 / [(σ_a / S_f) + (σ_m / S_u)]
```

Where:
- σ_a = stress amplitude = (σ_max - σ_min) / 2
- σ_m = mean stress = (σ_max + σ_min) / 2
- S_f = fatigue limit (≈ 0.4 × yield for steel)
- S_u = ultimate strength

Required minimum: **3.0** for coal support equipment

### Bearing Life (ISO 281)

For rolling element bearings:

```
L₁₀ = (C / P)³ × 10⁶ cycles
```

Where:
- C = dynamic load rating (function of bearing size)
- P = equivalent load

### Hertzian Contact Stress

For cylindrical bearing contact:

```
p_max = √(P × E / (π × d × (1 - ν²)))
```

Where:
- P = load
- E = elastic modulus
- d = contact diameter
- ν = Poisson's ratio

## Dynamic Simulation

### Equation of Motion

With mass distribution and damping:

```
I·α = τ_motor - τ_load - τ_damping
```

Where:
- I = effective moment of inertia at input crank
- α = angular acceleration
- τ_motor = torque from hydraulic pressure
- τ_load = resisting torque from coal load
- τ_damping = damping torque (proportional to velocity)

### Time Integration

Uses simple Euler method for first-order derivative approximation:

```
θ(t+Δt) = θ(t) + ω(t)·Δt
ω(t+Δt) = ω(t) + α(t)·Δt
```

For improved accuracy, higher-order methods (RK4) can be implemented.

---

## Material Properties (Typical)

**Structural Steel Q345** (common for coal support):
- Yield strength: 345 MPa
- Ultimate strength: 520 MPa
- Elastic modulus: 210 GPa
- Density: 7850 kg/m³
- Fatigue limit (R=-1): 138 MPa (0.4 × yield)

## Coal Mining Equipment Standards

**Chinese Standards**:
- GB/T TJ 3500-2011: Safety of hydraulic support equipment
- GB 6952: Hydraulic cylinders - Rod eye and head eye
- MT/T 1049: Cantilever equipment safety

**Key Requirements**:
- Static safety factor: ≥ 2.5
- Fatigue safety factor: ≥ 3.0  
- System pressure: 25 MPa (250 bar)
- Operating cycles: > 1 million for typical mine operation

---

## Usage Examples

See the `examples/` directory for complete working examples:

1. **example1_basic_configuration.py**: Basic linkage setup and analysis
2. **example2_dynamic_simulation.py**: Time-domain simulation
3. **example3_workspace_analysis.py**: Workspace and efficiency analysis

---

## API Overview

### Main Classes

```python
from coal4bar import (
    FourBarLinkage,      # Kinematic model
    ForceAnalysis,       # Static and dynamic forces
    DynamicSimulation,   # Time-domain simulation
    SafetyAnalyzer,      # Safety and reliability
    Visualizer           # Plots and visualization
)
```

### Quick Start

```python
from coal4bar import FourBarLinkage
from coal4bar.structure import FourBarDimensions
import math

# Define linkage
dims = FourBarDimensions(
    base_length=1000,      # mm
    input_crank=250,
    coupler=800,
    output_link=600
)

# Create linkage
linkage = FourBarLinkage(dims)

# Analyze at specific angle
linkage.forward_kinematics(math.radians(45))
print(f"Output position: {linkage.D}")
print(f"Output angle: {math.degrees(linkage.get_output_angle())}°")
```

---

## References

1. **Mechanism Theory**:
   - Erdman, A. G., & Sandor, G. N. (2016). Mechanism Design: Analysis and Synthesis (Vol. 1). Pearson.
   - Uicker, J. J., Pennock, G. R., & Shigley, J. E. (2016). Theory of Machines and Mechanisms.

2. **Coal Mining Standards**:
   - Coal Machinery Design Handbook (Chinese Mining Engineering Association)
   - ISO 281: Rolling bearings - Dynamic load ratings and fatigue life

3. **Hydraulic Systems**:
   - ISO 4413: Hydraulic fluid power systems - General rules and safety

4. **Numerical Analysis**:
   - Atkinson, K. E. (2008). An Introduction to Numerical Analysis. Wiley.

---

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! See CONTRIBUTING.md for guidelines.

## Support

For issues and questions:
- GitHub Issues: https://github.com/abelli5/coal4bar/issues
- Documentation: https://coal4bar.readthedocs.io
