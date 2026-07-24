import phasor as ph

laser = ph.Laser()
beam_splitter = ph.BeamSplitter()
detector_upper = ph.Detector()
detector_lower = ph.Detector()

circuit = ph.Circuit()
circuit.add_components(
    laser,
    beam_splitter,
    detector_upper,
    detector_lower,
)

circuit.connect(laser.output_port, beam_splitter.upper_input)
circuit.connect(beam_splitter.upper_output, detector_upper.input_port)
circuit.connect(beam_splitter.lower_output, detector_lower.input_port)

sim = ph.Simulator(circuit)
results = sim.run()
print(results)
