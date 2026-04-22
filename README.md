# coal4bar

**Four-Bar Hydraulic Support Simulation and Analysis Tool**

A comprehensive Python toolkit for analyzing and simulating four-bar linkage hydraulic supports used in coal mining operations. This project provides kinematic analysis, force analysis, dynamic simulation, and safety assessment for these critical mining support structures.

## Features

### 🔧 **Structural Analysis**
- Four-bar linkage geometry and kinematics
- Forward kinematic solution with constraint handling
- Grashof criterion validation for mechanism classification
- Workspace analysis and output trajectory tracking

### ⚙️ **Force Analysis**
- Static force equilibrium calculations
- Bearing load determination at all joints
- Hydraulic force requirement calculation
- Mechanical advantage mapping across working range
- Stress distribution in linkage members

### 🎬 **Dynamic Simulation**
- Time-domain kinematic and dynamic simulation
- Variable coal loading profiles
- Velocity and acceleration analysis
- Energy absorption during loading transients
- Fatigue life estimation using Miner's rule

### 🛡️ **Safety Assessment**
- Static and fatigue safety factor calculations
- Bearing contact stress analysis (Hertzian)
- Hydraulic system pressure verification
- ISO 281 bearing life prediction
- Structural stability evaluation

### 📊 **Visualization**
- Linkage configuration plots
- Workspace visualization
- Force vector diagrams
- Time-domain force and motion plots
- Mechanical advantage maps

## Installation

### From Source
```bash
git clone https://github.com/abelli5/coal4bar.git
cd coal4bar
pip install -e ".[dev]"
```

### Basic Installation
```bash
pip install coal4bar
```

## Quick Start

### Example 1: Basic Configuration Analysis

```python
from coal4bar import FourBarLinkage, ForceAnalysis
from coal4bar.structure import FourBarDimensions
import math

# Define linkage dimensions (in mm)
dimensions = FourBarDimensions(
    base_length=1000,      # Fixed frame
    input_crank=250,       # Hydraulic cylinder crank
    coupler=800,           # Intermediate link
    output_link=600        # Support leg
)

# Create linkage
linkage = FourBarLinkage(dimensions)

# Analyze at 45° input angle
linkage.forward_kinematics(math.radians(45))

# Perform force analysis with 50 kN coal load
analyzer = ForceAnalysis(linkage)
result = analyzer.analyze_static_forces(coal_force=50000)

print(f"Mechanical Advantage: {result['mechanical_advantage']:.3f}")
print(f"Required Hydraulic Force: {result['hydraulic_force']/1000:.1f} kN")
```

### Example 2: Dynamic Simulation

```python
from coal4bar import DynamicSimulation

# Create simulator
simulator = DynamicSimulation(linkage)

# Define coal loading profile
def coal_load(t):
    if t < 1.0:
        return 50000 * (t / 1.0)  # Ramp up
    else:
        return 50000  # Hold

# Run simulation
results = simulator.run_simulation(
    duration=2.0,
    dt=0.01,
    coal_force_profile=coal_load
)

print(f"Max Bearing Load: {results['max_bearing_load_A']:.0f} N")
print(f"Max Output Velocity: {results['max_output_velocity']:.4f} m/s")
```

### Example 3: Safety Analysis

```python
from coal4bar import SafetyAnalyzer

analyzer = SafetyAnalyzer(linkage)

# Check linkage stability
stability = analyzer.analyze_linkage_stability()
print(f"Mechanism Type: {stability['linkage_type']}")

# Analyze bearing safety
bearing_safety = analyzer.analyze_bearing_loads(max_bearing_load=50000)
print(f"Bearing Safety Factor: {bearing_safety['safety_factor_bearing']:.2f}")
```

## Project Structure

```
coal4bar/
├── coal4bar/                      # Main package
│   ├── __init__.py
│   ├── structure.py              # Kinematic geometry
│   ├── forces.py                 # Force analysis
│   ├── simulation.py             # Dynamic simulation
│   ├── visualization.py          # Plotting and visualization
│   └── safety_analysis.py        # Safety and reliability
├── tests/
│   └── test_coal4bar.py          # Unit tests
├── examples/
│   ├── example1_basic_configuration.py
│   ├── example2_dynamic_simulation.py
│   └── example3_workspace_analysis.py
├── docs/
│   └── PHYSICS_AND_THEORY.md     # Detailed documentation
├── pyproject.toml
├── setup.py
├── requirements.txt
└── README.md
```

## Technical Details

### Mathematical Foundation

The four-bar linkage is modeled using:

1. **Kinematic equations** - Position analysis via constraint solving
2. **Force analysis** - Static equilibrium and moment balance
3. **Dynamics** - Lagrangian mechanics with damping
4. **Safety standards** - Coal mining industry guidelines

### Material Properties

Default structural steel (Q345):
- Yield strength: 345 MPa
- Ultimate strength: 520 MPa
- Elastic modulus: 210 GPa
- Fatigue limit: 138 MPa (at 10⁶ cycles, R=-1)

### Design Standards

- Static safety factor: ≥ 2.5 (industry requirement)
- Fatigue safety factor: ≥ 3.0 (industry requirement)
- System pressure: 25 MPa (250 bar, typical)
- Operating life: > 1 million cycles

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ --cov=coal4bar --cov-report=html
```

## Performance

Simulation performance (typical 2-second simulation, dt=0.01s):
- Kinematic analysis: < 1 ms per step
- Force calculation: < 5 ms per step
- Complete simulation: ~200-300 ms

## Integration Ready

The project is designed for integration:
- **CAD Export**: STEP/IGES file generation for part modeling
- **LLM Integration**: Modular APIs for AI-assisted design
- **Data Export**: JSON/CSV output for spreadsheet analysis
- **Visualization**: matplotlib-based plots for documentation

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use coal4bar in research, please cite:

```bibtex
@software{coal4bar2024,
  title={coal4bar: Four-Bar Hydraulic Support Simulation and Analysis},
  author={abelli5},
  year={2024},
  url={https://github.com/abelli5/coal4bar}
}
```

## References

1. Erdman, A. G., & Sandor, G. N. (2016). Mechanism Design: Analysis and Synthesis. Pearson.
2. ISO 281:2023 Rolling bearings — Dynamic load ratings and fatigue life
3. GB/T TJ 3500-2011 Safety of hydraulic support systems for coal mining
4. Coal mining machinery design standards (China)

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/abelli5/coal4bar/issues)
- **Discussions**: [GitHub Discussions](https://github.com/abelli5/coal4bar/discussions)
- **Documentation**: [Full Documentation](docs/PHYSICS_AND_THEORY.md)

---

**Version**: 0.1.0  
**Status**: Alpha (Active Development)  
**Last Updated**: April 2024
