import math

from phasor.components.beam_splitter import BeamSplitter
from phasor.components.detector import Detector
from phasor.components.laser import Laser
from phasor.network.circuit import Circuit
from phasor.physics.optical_field import OpticalField
from phasor.simulation.simulator import Simulator


def test_beam_splitter_conserves_power():
    laser = Laser(field=OpticalField(1 + 2j))
    splitter = BeamSplitter()

    d1 = Detector()
    d2 = Detector()

    circuit = Circuit()

    circuit.add_components(laser, splitter, d1, d2)

    input_waveguide = circuit.connect(laser.output_port, splitter.input_ports[0])

    upper = circuit.connect(splitter.output_ports[0], d1.input_port)

    lower = circuit.connect(splitter.output_ports[1], d2.input_port)

    Simulator(circuit).run()
    if upper.field is None or lower.field is None or input_waveguide.field is None:
        raise RuntimeError("Field is None")
    assert math.isclose(upper.field.intensity, lower.field.intensity, rel_tol=1e-12)

    assert math.isclose(
        upper.field.intensity + lower.field.intensity,
        input_waveguide.field.intensity,
        rel_tol=1e-12,
    )
