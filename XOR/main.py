import NEAT


# XOR inputs and expected outputs
xor_inputs = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]
xor_outputs = [(0.0,), (1.0,), (1.0,), (0.0,)]


def fitness(population):

    """ XOR fitness function """

    for agent in population:
        agent.fitness = 4.0
        for inputs, e_out in zip(xor_inputs, xor_outputs):
            a_out = agent.evaluate(inputs)[0]
            agent.fitness -= (e_out[0] - a_out)**2


def run(config_file):

    """ Creates the config object and starts the app. """

    config = NEAT.Config(config_file)
    NEAT.App(config, fitness)


if __name__ == "__main__":
    run("config.txt")

