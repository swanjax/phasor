from __future__ import annotations

from phasor.components.component import Component
from phasor.network.port import Port
from phasor.network.port_direction import PortDirection
from phasor.network.waveguide import Waveguide


class Circuit:
    """
    Represent a photonic circuit as a graph of component connected by waveguides.
    """

    def __init__(self):
        self._components: list[Component] = []
        self._waveguides: list[Waveguide] = []

    @property
    def components(self) -> tuple[Component, ...]:
        return tuple(self._components)

    @property
    def waveguides(self) -> tuple[Waveguide, ...]:
        return tuple(self._waveguides)

    def add_component(self, component: Component) -> None:
        if component in self._components:
            raise ValueError("Component already exists in circuit.")
        self._components.append(component)

    def connect(self, source: Port, destination: Port) -> Waveguide:
        if source.component not in self._components:
            raise ValueError("Source component is not in the circuit.")

        if destination.component not in self._components:
            raise ValueError("Destination component is not in the circuit.")

        if source.direction is not PortDirection.OUTPUT:
            raise ValueError("Source port must be an OUTPUT port.")

        if destination.direction is not PortDirection.INPUT:
            raise ValueError("Destination port must be an INPUT port.")

        if source.component is destination.component:
            raise ValueError("Cannot connect a component to itself.")

        waveguide = Waveguide(source, destination)
        source.connect(waveguide)
        destination.connect(waveguide)
        self._waveguides.append(waveguide)

        return waveguide
