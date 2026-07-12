from abc import ABC, abstractmethod

from phasor.components.component import Component
from phasor.network.circuit import Circuit
from phasor.network.port import Port
from phasor.network.port_direction import PortDirection


class CompositeComponent(Component, ABC):
    def __init__(
        self, port_directions: tuple[PortDirection, ...], name: str | None = None
    ):
        super().__init__(port_directions=port_directions, name=name)
        self._subcircuit = Circuit()
        self._port_map = {}

    @property
    def sub_circuit(self) -> Circuit:
        return self._subcircuit

    @property
    def port_map(self) -> dict[Port, Port]:
        return self._port_map

    def set_port_map(self, mapping: dict[Port, Port]) -> None:
        internal_ports = {
            port
            for component in self.sub_circuit.components
            for port in component.ports
        }

        if len(set(mapping.values())) != len(mapping):
            raise ValueError("Each internal port may be mapped at most once.")

        for ext_port, int_port in mapping.items():
            if ext_port not in self.ports:
                raise ValueError(
                    f"{ext_port} is not an external port of this component."
                )

            if int_port not in internal_ports:
                raise ValueError(f"{int_port} does not belong to the subcircuit.")

            if ext_port.direction is not int_port.direction:
                raise ValueError(
                    "External and internal ports must have the same direction."
                )

        self._port_map = dict(mapping)

    @abstractmethod
    def clone(self) -> Component:
        pass
