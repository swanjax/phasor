from __future__ import annotations

from phasor.components.component import Component
from phasor.network.port_direction import PortDirection
from phasor.physics.optical_field import OpticalField
from phasor.network.port import Port

class PhaseShifter(Component):
    '''
    Applies a phase shift to an incoming optical field.
    '''

    def __init__(
        self,
        phi: float,
        name: str | None = None
    ):
        super().__init__(
            port_directions=(
                PortDirection.INPUT,
                PortDirection.OUTPUT
            ),
            name=name
        )
        self._phi = phi

    @property
    def phi(self) -> float:
        return self._phi

    @property
    def input_port(self) -> Port:
        return self.ports[0]

    @property
    def output_port(self) -> Port:
        return self.ports[1]

    def transform(self, field: OpticalField) -> OpticalField:
        '''
        Apply the configured phase shift.
        '''
        return field.phase_shift(self.phi)
