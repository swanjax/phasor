import math

from phasor.components.beam_splitter import BeamSplitter
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
    circuit.add_component(laser)
    circuit.add_component(detector)

    circuit.connect(
        laser.output_port,
        detector.input_port,
    )

    simulator = Simulator(circuit)

    assert simulator._topological_sort() == [
        laser,
        detector,
    ]


def test_topological_sort_linear():
    laser = Laser()
    phase = PhaseShifter(phi=1.57)
    detector = Detector()

    circuit = Circuit()

    for component in (laser, phase, detector):
        circuit.add_component(component)

    circuit.connect(
        laser.output_port,
        phase.input_port,
    )

    circuit.connect(
        phase.output_port,
        detector.input_port,
    )

    simulator = Simulator(circuit)

    assert simulator._topological_sort() == [
        laser,
        phase,
        detector,
    ]


def test_laser_emits_field():
    laser = Laser(field=OpticalField(1 + 2j))
    detector = Detector()
    circuit = Circuit()
    circuit.add_component(laser)
    circuit.add_component(detector)

    waveguide = circuit.connect(laser.output_port, detector.input_port)

    simulator = Simulator(circuit)
    simulator.run()

    assert waveguide.field is not None
    assert waveguide.field == laser.field


def test_phase_shifter():
    laser = Laser(field=OpticalField(1 + 2j))
    phase_shifter = PhaseShifter(phi=math.pi)
    detector = Detector()
    circuit = Circuit()
    circuit.add_component(laser)
    circuit.add_component(phase_shifter)
    circuit.add_component(detector)

    circuit.connect(laser.output_port, phase_shifter.input_port)
    waveguidePD = circuit.connect(phase_shifter.output_port, detector.input_port)

    simulator = Simulator(circuit)
    simulator.run()

    expected_wave = OpticalField(-1 - 2j)
    assert waveguidePD.field is not None
    assert waveguidePD.field == expected_wave


def test_detector():
    laser = Laser(field=OpticalField(1 + 2j))
    detector = Detector()
    circuit = Circuit()
    circuit.add_component(laser)
    circuit.add_component(detector)

    waveguide = circuit.connect(laser.output_port, detector.input_port)

    simulator = Simulator(circuit)
    results = simulator.run()

    assert waveguide.field is not None
    assert waveguide.field == laser.field
    assert detector.input_port.waveguide is not None
    assert waveguide.field == detector.input_port.waveguide.field
    assert math.isclose(results[detector], laser.field.intensity, rel_tol=1e-12)


def test_beam_splitter():
    laser = Laser(field=OpticalField(1 + 2j))
    beam_splitter = BeamSplitter()
    detect1 = Detector()
    detect2 = Detector()
    circuit = Circuit()
    circuit.add_component(laser)
    circuit.add_component(beam_splitter)
    circuit.add_component(detect1)
    circuit.add_component(detect2)
    waveguide1 = circuit.connect(laser.output_port, beam_splitter.input_ports[0])
    waveguide2 = circuit.connect(beam_splitter.output_ports[0], detect1.input_port)
    waveguide3 = circuit.connect(beam_splitter.output_ports[1], detect2.input_port)
    simulator = Simulator(circuit)
    simulator.run()

    assert waveguide1.field is not None
    assert waveguide2.field is not None
    assert waveguide3.field is not None

    input_intensity = waveguide1.field.intensity
    upper_intensity = waveguide2.field.intensity
    lower_intensity = waveguide3.field.intensity

    assert math.isclose(
        upper_intensity,
        lower_intensity,
        rel_tol=1e-12,
    )

    assert math.isclose(
        upper_intensity + lower_intensity,
        input_intensity,
        rel_tol=1e-12,
    )
