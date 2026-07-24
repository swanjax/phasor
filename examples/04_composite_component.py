"""
Composite Component

This example demonstrates how to create a reusable component by
subclassing `CompositeComponent`.

The `SinglePhase` component wraps a `PhaseShifter` while exposing the
same input and output interface. Composite components can be reused just
like any other Phasor component.
"""

import math

import phasor as ph
from phasor.network.port import PortDirection


class SinglePhase(ph.CompositeComponent):
    """A reusable single phase shifter."""

    def __init__(self, phi: float):
        super().__init__(
            port_directions=(
                PortDirection.INPUT,
                PortDirection.OUTPUT,
            )
        )
        self._phi = phi
        phase = ph.PhaseShifter(phi)
        self.sub_circuit.add_component(phase)
        self.set_port_map(
            {
                self.input_port: phase.input_port,
                self.output_port: phase.output_port,
            }
        )

    @property
    def input_port(self):
        return self.input_ports[0]

    @property
    def output_port(self):
        return self.output_ports[0]

    def clone(self):
        return SinglePhase(self._phi)


# Using a composite component in a circuit
laser = ph.Laser()
phase = SinglePhase(math.pi / 2)
detector = ph.Detector()

circuit = ph.Circuit()
circuit.add_components(
    laser,
    phase,
    detector,
)

circuit.connect(
    laser.output_port,
    phase.input_port,
)

circuit.connect(
    phase.output_port,
    detector.input_port,
)

# flatten the composite circuit before simulation
flat = circuit.flatten()
simulator = ph.Simulator(flat)

print(simulator.run())
