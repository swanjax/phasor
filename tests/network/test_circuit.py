import pytest

from phasor.components.detector import Detector
from phasor.components.laser import Laser
from phasor.network.circuit import Circuit


def test_add_component():
    laser = Laser()

    circuit = Circuit()
    circuit.add_component(laser)

    assert laser in circuit.components
    assert len(circuit.components) == 1


def test_add_components():
    laser = Laser()
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, detector)

    assert len(circuit.components) == 2
    assert laser in circuit.components
    assert detector in circuit.components


def test_duplicate_component_raises():
    laser = Laser()

    circuit = Circuit()
    circuit.add_component(laser)

    with pytest.raises(ValueError):
        circuit.add_component(laser)


def test_duplicate_component_in_batch_raises():
    laser = Laser()

    circuit = Circuit()

    with pytest.raises(ValueError):
        circuit.add_components(laser, laser)


def test_connect_creates_waveguide():
    laser = Laser()
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, detector)

    waveguide = circuit.connect(laser.output_port, detector.input_port)

    assert waveguide in circuit.waveguides
    assert waveguide.source == laser.output_port
    assert waveguide.destination == detector.input_port


def test_port_cannot_have_multiple_connections():
    laser1 = Laser()
    laser2 = Laser()
    detector = Detector()

    circuit = Circuit()

    circuit.add_components(laser1, laser2, detector)

    circuit.connect(laser1.output_port, detector.input_port)

    with pytest.raises(RuntimeError):
        circuit.connect(laser2.output_port, detector.input_port)
