"""
Mach–Zehnder Interferometer

This example demonstrates how to construct and simulate a Mach–Zehnder
interferometer (MZI) using Phasor.

A coherent optical field is split into two paths by the first beam splitter.
One arm contains a phase shifter before the two paths are recombined by a
second beam splitter. The resulting interference pattern is observed by two
detectors.

This example introduces:
    - Beam splitters
    - Phase shifters
    - Multi-path optical circuits
    - Multiple detectors
"""

import math

import phasor as ph

laser = ph.Laser()

splitter = ph.BeamSplitter()
phase_shifter = ph.PhaseShifter(phi=math.pi / 2)
combiner = ph.BeamSplitter()

upper_detector = ph.Detector()
lower_detector = ph.Detector()

circuit = ph.Circuit()
circuit.add_components(
    laser,
    splitter,
    phase_shifter,
    combiner,
    upper_detector,
    lower_detector,
)

# Split the incoming optical field
circuit.connect(laser.output_port, splitter.upper_input)

# Upper arm (with phase shift)
circuit.connect(splitter.upper_output, phase_shifter.input_port)
circuit.connect(phase_shifter.output_port, combiner.upper_input)

# Lower arm (reference path)
circuit.connect(splitter.lower_output, combiner.lower_input)

# Detect the recombined outputs
circuit.connect(combiner.upper_output, upper_detector.input_port)
circuit.connect(combiner.lower_output, lower_detector.input_port)

simulator = ph.Simulator(circuit)
results = simulator.run()

print(results)
