import random
from operator import attrgetter


class Selector:

    """ Contains the methods to select a parent from a list of agents. """

    def __init__(self, parents):
        self.__parents = parents
        self.__max_fitness = max(parents, key=attrgetter("fitness")).fitness

    def sto_acc(self):

        """ Selects and returns an agent from a list of agents using
            stochastic acceptance. """

        while True:
            parent = random.choice(self.__parents)
            if random.random() < parent.fitness / self.__max_fitness:
                return parent
