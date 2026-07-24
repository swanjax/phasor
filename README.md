# Phasor
Phasor is a python library for building and simulating photonic circuits using coherent optical fields.

It provides a clean, modular API for constructing optical circuits from reusable components such as lasers, beam splitters, phase shifters, and detectors. Phasor is designed to be intuitive, extensible and fully types, making it suitable for experimentation, prototyping, and as a foundation for future research in photonic computing.

> Phasor is in active development. Version 0.1.0 provvides the core building blocks for constructing and simulating photonic circuits. The public API may evolve before a stable 1.0 release.

## Features 
- Modular, component-based circuit construction.
- Simulation of coherent optical field propagation.
- Reusable hierarchical circuits using `CompositeComponent`.
- Recursive circuit flattening for nested components during simulation time.
- Extensible architecture for implementing custom photonic components.

## Installation
Clone the repository and install it locally.
```bash
git clone https://github.com/swanjax/phasor.git
cd phasor

pip install -e ".[dev]"
```

## Quick Start
The primary public API is exposed directly from the `phasor` package.

```python
import phasor as ph

# Create the optical field emitted by the laser
field = ph.OpticalField(
    amplitude=1.0,
    phase=0.0,
)

# Create the circuit components
laser = ph.Laser(field)
detector = ph.Detector()

# Assemble the circuit
circuit = ph.Circuit()
circuit.add_components(laser, detector)
circuit.connect(laser.output_port, detector.input_port)

# Simulate the circuit
simulator = ph.Simulator(circuit)
results = simulator.run()

# Inspect the detector output
print(results)
```
This example demonstrates a typical workflow when using Phasor:
1. Create an `OpticalField`.
2. Instantiate required components.
3. Add components to a `Circuit`.
4. Connect relevant component ports.
5. Initialise and run the `Simulator`.
6. Inspect the simulation result through detectors.

## Core Concepts
### OpticalField
`OpticalField` represents a coherent optical field that travels through a circuit. It stores the _physical_ properties propagated between components during simulation.

### Components
Phasor currently provides the following primitive components:
- `Laser`
- `BeamSplitter`
- `PhaseShifter`
- `Detector`

Each of these components exposes a collection of input and output ports that are used to construct the circuit.

### Circuit
A `Circuit` stores the network of connected components.
Components are added using:
`circuit.connect(source_port, destination_port)`

### Simulator
`Simulator` executes the circuit by propagating optical fields through the component graph.

### CompositeComponent
`CompositeComponent` allows multiple primitive components to be combined as a "mini-circcuit" to be reusable higher-level building blocks.

Composite components can be nested and are recursively flattened before simulation.
