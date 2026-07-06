from __future__ import annotations

from typing import TYPE_CHECKING

from phasor.network.port_direction import PortDirection

if TYPE_CHECKING:
    from phasor.components.component import Component
    from phasor.network.waveguide import Waveguide


class Port:
    """
    Connection point on a component.
    """

    def __init__(self, component: Component, index: int, direction: PortDirection):
        self._component = component
        self._index = index
        self._direction = direction
        self._waveguide: Waveguide | None = None

    @property
    def component(self) -> Component:
        return self._component

    @property
    def index(self) -> int:
        return self._index

    @property
    def direction(self) -> PortDirection:
        return self._direction

    @property
    def waveguide(self) -> Waveguide | None:
        return self._waveguide

    def connect(self, waveguide: Waveguide) -> None:
        if self._waveguide is not None:
            raise RuntimeError("Port is already connected.")
        self._waveguide = waveguide

    def __repr__(self) -> str:
        return (
            f"Port(component={self.component.name}, "
            f"index={self.index}, "
            f"direction={self.direction.name}) "
        )
