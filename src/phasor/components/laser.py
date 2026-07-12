from __future__ import annotations

from phasor.components.component import Component
from phasor.network.port import Port
from phasor.network.port_direction import PortDirection
from phasor.physics.optical_field import OpticalField


class Laser(Component):
    """
    Ideal coherent laser source
    """

    def __init__(self, field: OpticalField | None = None, name: str | None = None):
        super().__init__(port_directions=(PortDirection.OUTPUT,), name=name)
        self._field = field if field is not None else OpticalField(1 + 0j)

    @property
    def field(self) -> OpticalField:
        return self._field

    @property
    def output_port(self) -> Port:
        return self.ports[0]

    def emit(self) -> OpticalField:
        """
        Emit the laser's optical field.
        """
        return self.field

    def clone(self) -> Laser:
        return Laser(
            field=self.field,
        )
