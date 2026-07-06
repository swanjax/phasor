from __future__ import annotations
from abc import ABC
from uuid import UUID, uuid4

from phasor.network.port import Port
from phasor.network.port_direction import PortDirection

class Component(ABC):
    '''
    Base class for every physical component.
    '''
    def __init__(
        self,
        port_directions: tuple[PortDirection, ...],
        name: str | None = None
    ):
        self._id: UUID = uuid4()
        self._name = name if name is not None else f"{self.__class__.__name__}_{self.id.hex[:8]}"
        self._ports = tuple(
            Port(self, index, direction) for index, direction in enumerate(port_directions)
        )

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def ports(self) -> tuple[Port, ...]:
        return self._ports

    @property
    def input_ports(self) -> tuple[Port, ...]:
        in_ports = []
        for port in self._ports:
            if port.direction is PortDirection.INPUT:
                in_ports.append(port)
        return tuple(in_ports)

    @property
    def output_ports(self) -> tuple[Port, ...]:
        out_ports = []
        for port in self._ports:
            if port.direction is PortDirection.OUTPUT:
                out_ports.append(port)
        return tuple(out_ports)
