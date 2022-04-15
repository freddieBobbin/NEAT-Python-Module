from NEAT import NetLoader

xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]

net = NetLoader.load_net("corys_net")

for inputs in xor_inputs:
    print(inputs, net.evaluate(inputs))

