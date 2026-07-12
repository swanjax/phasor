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

    def add_components(self, *components) -> None:
        for component in components:
            self.add_component(component)

    def add_component(self, component: Component) -> None:
        if component in self._components:
            raise ValueError(f"{component} already exists in circuit.")
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

    def _flatten_into(
        self, flat: Circuit, clone_map: dict[Component, Component]
    ) -> None:
        from phasor.components.composite_component import CompositeComponent

        def resolve(port: Port):
            component = port.component
            if isinstance(component, CompositeComponent):
                internal_port = component.port_map[port]
                return resolve(internal_port)
            else:
                return port

        for comp in self._components:
            if isinstance(comp, CompositeComponent):
                comp.sub_circuit._flatten_into(flat, clone_map)
            else:
                clone = comp.clone()
                flat.add_component(clone)
                clone_map[comp] = clone

        for wg in self.waveguides:
            src = wg.source
            p_src = resolve(src)
            c_s = clone_map[p_src.component]
            new_src = c_s.ports[p_src.index]

            dst = wg.destination
            p_dst = resolve(dst)
            c_d = clone_map[p_dst.component]
            new_dst = c_d.ports[p_dst.index]

            flat.connect(source=new_src, destination=new_dst)

    def flatten(self) -> Circuit:
        flat = Circuit()
        clone_map = {}
        self._flatten_into(flat, clone_map)
        return flat
