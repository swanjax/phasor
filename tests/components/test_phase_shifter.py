import math

from phasor.components.detector import Detector
from phasor.components.laser import Laser
from phasor.components.phase_shifter import PhaseShifter
from phasor.network.circuit import Circuit
from phasor.physics.optical_field import OpticalField
from phasor.simulation.simulator import Simulator


def test_phase_shifter_rotates_field():
    laser = Laser(field=OpticalField(1 + 2j))
    phase = PhaseShifter(phi=math.pi)
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, phase, detector)

    circuit.connect(laser.output_port, phase.input_port)

    output = circuit.connect(phase.output_port, detector.input_port)

    Simulator(circuit).run()

    expected = OpticalField(-1 - 2j)

    assert output.field is not None
    assert output.field == expected
