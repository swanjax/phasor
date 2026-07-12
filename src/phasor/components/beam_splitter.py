from __future__ import annotations

from cmath import sqrt

from phasor.components.component import Component
from phasor.network.port import Port
from phasor.network.port_direction import PortDirection
from phasor.physics.optical_field import OpticalField


class BeamSplitter(Component):
    """
    Splits beam from 2 inputs to 2 outputs, while conserving total power.
    """

    def __init__(self, reflectivity: float = 0.5, name: str | None = None):
        super().__init__(
            port_directions=(
                PortDirection.INPUT,
                PortDirection.INPUT,
                PortDirection.OUTPUT,
                PortDirection.OUTPUT,
            ),
            name=name,
        )
        if not 0.0 <= reflectivity <= 1.0:
            raise ValueError("Reflectivity must be between 0 and 1.")
        self._reflectivity = reflectivity

    @property
    def upper_input(self) -> Port:
        return self.ports[0]

    @property
    def lower_input(self) -> Port:
        return self.ports[1]

    @property
    def upper_output(self) -> Port:
        return self.ports[2]

    @property
    def lower_output(self) -> Port:
        return self.ports[3]

    @property
    def reflectivity(self) -> float:
        return self._reflectivity

    def transform(
        self, upper_field: OpticalField, lower_field: OpticalField
    ) -> tuple[OpticalField, OpticalField]:
        r = sqrt(self._reflectivity)
        t = sqrt(1 - self._reflectivity)
        out1 = t * upper_field + 1j * r * lower_field
        out2 = 1j * r * upper_field + t * lower_field
        return (out1, out2)

    def clone(self) -> BeamSplitter:
        return BeamSplitter(reflectivity=self.reflectivity)
