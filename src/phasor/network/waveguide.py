from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from phasor.network.port import Port
    from phasor.physics.optical_field import OpticalField

class Waveguide:
    '''
    Carries the optical field between a source port and destination port.
    '''

    def __init__(self, source: Port, destination: Port):
        self._source = source
        self._destination = destination
        self._field: OpticalField | None = None

    @property
    def source(self) -> Port:
        return self._source

    @property
    def destination(self) -> Port:
        return self._destination

    @property
    def field(self) -> OpticalField | None:
        return self._field

    @field.setter
    def field(self, field: OpticalField | None) -> None:
        self._field = field

    def __repr__(self) -> str:
        return (
            f"Waveguide(source={self.source}, "
            f"destination={self.destination})"
        )
