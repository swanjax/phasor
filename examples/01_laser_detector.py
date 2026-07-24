import phasor as ph

laser = ph.Laser()
detector = ph.Detector()
circuit = ph.Circuit()
circuit.add_components(laser, detector)

circuit.connect(laser.output_port, detector.input_port)

sim = ph.Simulator(circuit)
results = sim.run()
print(results)
