import math

from phasor.components.composite_component import CompositeComponent
from phasor.components.detector import Detector
from phasor.components.laser import Laser
from phasor.components.phase_shifter import PhaseShifter
from phasor.network.circuit import Circuit
from phasor.network.port_direction import PortDirection
from phasor.physics.optical_field import OpticalField
from phasor.simulation.simulator import Simulator


class SinglePhase(CompositeComponent):
    def __init__(self, phi):
        super().__init__(port_directions=(PortDirection.INPUT, PortDirection.OUTPUT))
        self._phi = phi
        phase = PhaseShifter(phi)

        self.sub_circuit.add_component(phase)
        self.set_port_map(
            {
                self.input_ports[0]: phase.input_port,
                self.output_ports[0]: phase.output_port,
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


def test_flatten_single_level_composite():
    laser = Laser()
    phase = SinglePhase(math.pi)
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, phase, detector)

    circuit.connect(laser.output_port, phase.input_port)
    circuit.connect(phase.output_port, detector.input_port)

    flat = circuit.flatten()

    assert all(not isinstance(c, CompositeComponent) for c in flat.components)
    assert len(flat.components) == 3
    assert len(flat.waveguides) == 2


def test_flatten_preserves_original():
    phase = SinglePhase(math.pi)

    circuit = Circuit()
    circuit.add_component(phase)
    flat = circuit.flatten()

    assert phase in circuit.components
    assert phase not in flat.components


def test_flatten_contains_internal_components():
    phase = SinglePhase(math.pi)

    circuit = Circuit()
    circuit.add_component(phase)
    flat = circuit.flatten()

    assert any(isinstance(c, PhaseShifter) for c in flat.components)


def test_flatten_preserves_simulation():
    laser = Laser(field=OpticalField(1 + 2j))
    phase = SinglePhase(math.pi)
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, phase, detector)

    circuit.connect(laser.output_port, phase.input_port)
    circuit.connect(phase.output_port, detector.input_port)

    flat = circuit.flatten()
    results = Simulator(flat).run()

    flat_detector = next(c for c in flat.components if isinstance(c, Detector))

    assert math.isclose(results[flat_detector], 5.0, rel_tol=1e-12)


class DoublePhase(CompositeComponent):
    def __init__(self, phi1, phi2):
        super().__init__(port_directions=(PortDirection.INPUT, PortDirection.OUTPUT))
        self.phi1 = phi1
        self.phi2 = phi2
        phase1 = SinglePhase(phi1)
        phase2 = SinglePhase(phi2)

        self.sub_circuit.add_components(phase1, phase2)

        self.sub_circuit.connect(phase1.output_port, phase2.input_port)

        self.set_port_map(
            {
                self.input_ports[0]: phase1.input_port,
                self.output_ports[0]: phase2.output_port,
            }
        )

    def clone(self):
        return DoublePhase(self.phi1, self.phi2)


def test_flatten_nested_composite():
    laser = Laser(field=OpticalField(1 + 2j))
    double_phase = DoublePhase(math.pi, math.pi)
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, double_phase, detector)

    circuit.connect(laser.output_port, double_phase.input_ports[0])
    circuit.connect(double_phase.output_ports[0], detector.input_port)

    flat = circuit.flatten()
    assert all(not isinstance(c, CompositeComponent) for c in flat.components)
    assert len(flat.components) == 4
    # Laser + PhaseShifter + PhaseShifter + Detector

    assert len(flat.waveguides) == 3
    results = Simulator(flat).run()

    flat_detector = next(c for c in flat.components if isinstance(c, Detector))

    assert math.isclose(results[flat_detector], 5.0, rel_tol=1e-12)
