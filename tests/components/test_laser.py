from phasor.components.detector import Detector
from phasor.components.laser import Laser
from phasor.network.circuit import Circuit
from phasor.physics.optical_field import OpticalField
from phasor.simulation.simulator import Simulator


def test_laser_emits_field():
    field = OpticalField(1 + 2j)

    laser = Laser(field=field)
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, detector)

    waveguide = circuit.connect(laser.output_port, detector.input_port)

    Simulator(circuit).run()

    assert waveguide.field is not None
    assert waveguide.field == field
