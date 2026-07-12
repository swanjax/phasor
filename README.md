# Phasor
A Python library for simulating photonic circuits using coherent optical fields.

## API Conventions
- Every component exposes a tuple of ports via `ports`.
- `input_ports` and `output_ports` provide filtered views of `ports`.
- Component-specific properties (for example, `upper_input` on `BeamSplitter`) are aliases for entries in `ports`; they do not represent distinct ports. Helping with intuitive construction of the circuit.
- Circuits are assembled by adding components using `Circuit.add_components(*components)` and connecting ports with `Circuit.connect(source_port, destination_port)`.
