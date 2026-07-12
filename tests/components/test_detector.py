import math

from phasor.components.detector import Detector
from phasor.components.laser import Laser
from phasor.network.circuit import Circuit
from phasor.physics.optical_field import OpticalField
from phasor.simulation.simulator import Simulator


def test_detector_measures_intensity():
    laser = Laser(field=OpticalField(1 + 2j))
    detector = Detector()

    circuit = Circuit()
    circuit.add_components(laser, detector)

    waveguide = circuit.connect(laser.output_port, detector.input_port)

    results = Simulator(circuit).run()

    assert waveguide.field == laser.field

    assert math.isclose(results[detector], 5.0, rel_tol=1e-12)
