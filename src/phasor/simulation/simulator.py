from collections import deque

from phasor.components.beam_splitter import BeamSplitter
from phasor.components.component import Component
from phasor.components.detector import Detector
from phasor.components.laser import Laser, OpticalField
from phasor.components.phase_shifter import PhaseShifter
from phasor.network.circuit import Circuit


class Simulator:
    def __init__(self, circuit: Circuit):
        self._circuit = circuit

    def _build_adjacency(self) -> dict[Component, list[Component]]:
        adjacency = {component: [] for component in self._circuit.components}
        for waveguide in self._circuit.waveguides:
            source_cmpt = waveguide.source.component
            destination_cmpt = waveguide.destination.component
            adjacency[source_cmpt].append(destination_cmpt)
        return adjacency

    def _compute_indegrees(
        self, adjacency: dict[Component, list[Component]]
    ) -> dict[Component, int]:
        indegrees = {component: 0 for component in adjacency}

        for neighbours in adjacency.values():
            for neighbour in neighbours:
                indegrees[neighbour] += 1

        return indegrees

    def _topological_sort(self) -> list[Component]:
        adjacency = self._build_adjacency()
        indegrees = self._compute_indegrees(adjacency)

        queue = deque(
            component for component, indegree in indegrees.items() if indegree == 0
        )

        exec_order = []

        while queue:
            cmpt = queue.popleft()
            exec_order.append(cmpt)

            for neighbour in adjacency[cmpt]:
                indegrees[neighbour] -= 1
                if indegrees[neighbour] == 0:
                    queue.append(neighbour)

        if len(exec_order) != len(self._circuit.components):
            raise RuntimeError("Circuit contains a cycle.")

        return exec_order

    def run(self) -> dict[Detector, float]:
        execution_order = self._topological_sort()
        results = {}
        for component in execution_order:
            if isinstance(component, Laser):
                field = component.emit()
                waveguide = component.output_port.waveguide
                if waveguide is None:
                    raise RuntimeError("Laser output port is not connected.")
                waveguide.field = field

            elif isinstance(component, PhaseShifter):
                waveguide_in = component.input_ports[0].waveguide
                if waveguide_in is None:
                    raise RuntimeError("Phase Shifter input port is not connected.")
                input_field = waveguide_in.field
                if input_field is None:
                    raise RuntimeError(
                        f"No optical field at {component.input_ports[0]}"
                    )
                output_field = component.transform(field=input_field)
                waveguide_out = component.output_ports[0].waveguide
                if waveguide_out is None:
                    raise RuntimeError("Phase Shifter output port is not connected.")
                waveguide_out.field = output_field

            elif isinstance(component, Detector):
                waveguide = component.input_ports[0].waveguide
                if waveguide is None:
                    raise RuntimeError("Detector input port is not connected.")
                input_field = waveguide.field
                if input_field is None:
                    raise RuntimeError(
                        f"No optical field at {component.input_ports[0]}"
                    )
                results[component] = component.measure(field=input_field)

            elif isinstance(component, BeamSplitter):
                upper_input_guide = component.upper_input.waveguide
                lower_input_guide = component.lower_input.waveguide

                if upper_input_guide is None or upper_input_guide.field is None:
                    upper_input_field = OpticalField(0j)
                else:
                    upper_input_field = upper_input_guide.field

                if lower_input_guide is None or lower_input_guide.field is None:
                    lower_input_field = OpticalField(0j)
                else:
                    lower_input_field = lower_input_guide.field

                upper_output_field, lower_output_field = component.transform(
                    upper_field=upper_input_field,
                    lower_field=lower_input_field,
                )

                upper_output = component.upper_output.waveguide
                if upper_output is not None:
                    upper_output.field = upper_output_field

                lower_output = component.lower_output.waveguide
                if lower_output is not None:
                    lower_output.field = lower_output_field

        return results
