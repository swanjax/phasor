import math

from phasor.components.detector import Detector
from phasor.components.laser import Laser
from phasor.components.phase_shifter import PhaseShifter
from phasor.network.circuit import Circuit
from phasor.physics.optical_field import OpticalField
from phasor.simulation.simulator import Simulator


def test_topological_sort_simple():
    laser = Laser()
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, detector)
    circuit.connect(laser.output_port, detector.input_port)
    simulator = Simulator(circuit)
    assert simulator._topological_sort() == [laser, detector]


def test_topological_sort_linear():
    laser = Laser()
    phase = PhaseShifter(phi=math.pi)
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, phase, detector)

    circuit.connect(laser.output_port, phase.input_port)
    circuit.connect(phase.output_port, detector.input_port)

    simulator = Simulator(circuit)
    assert simulator._topological_sort() == [laser, phase, detector]


def test_simulation_propagates_field():
    field = OpticalField(1 + 2j)
    laser = Laser(field=field)
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, detector)

    waveguide = circuit.connect(laser.output_port, detector.input_port)

    Simulator(circuit).run()

    assert waveguide.field is not None
    assert waveguide.field == field


def test_simulation_runs_linear_chain():
    laser = Laser(field=OpticalField(1 + 2j))
    phase = PhaseShifter(phi=math.pi)
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, phase, detector)

    circuit.connect(laser.output_port, phase.input_port)
    waveguide = circuit.connect(phase.output_port, detector.input_port)
    Simulator(circuit).run()
    assert waveguide.field == OpticalField(-1 - 2j)


def test_simulation_returns_detector_results():
    laser = Laser(field=OpticalField(1 + 2j))
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, detector)

    circuit.connect(laser.output_port, detector.input_port)
    results = Simulator(circuit).run()

    assert detector in results
    assert math.isclose(results[detector], 5.0, rel_tol=1e-12)
