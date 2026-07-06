from phasor.components.component import Component
from phasor.network.port_direction import PortDirection
from phasor.physics.optical_field import OpticalField
from phasor.network.port import Port

class Detector(Component):
    '''
    Ideal optical detector
    '''
    def __init__(
        self,
        name: str | None = None
    ):
        super().__init__(
            port_directions=(PortDirection.INPUT,),
            name=name
        )

    @property
    def input_port(self) -> Port:
        return self.ports[0]

    def measure(
        self,
        field: OpticalField,
    ) -> float:
        '''
        Measure the intensity of optical field.
        '''
        return field.intensity
