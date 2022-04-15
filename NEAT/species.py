from operator import attrgetter


class Species:

    """ Stores the data related to one species. Contains the methods to
        filter parents and add agents to the species. """

    @property
    def id(self):
        return self.__id

    @property
    def agents(self):
        return self.__agents

    @property
    def allowed_offspring(self):
        return self.__allowed_offspring

    @allowed_offspring.setter
    def allowed_offspring(self, value):
        self.__allowed_offspring = value

    @property
    def size(self):
        return self.__size

    @property
    def gens_since_imp(self):
        return self.__gens_since_imp

    @gens_since_imp.setter
    def gens_since_imp(self, value):
        self.__gens_since_imp = value

    @property
    def avg_fitness(self):
        return self.__avg_fitness

    @avg_fitness.setter
    def avg_fitness(self, value):
        self.__avg_fitness = value

    def __init__(self, species_id, agent, avg_fitness=0, gens_since_imp=0):
        self.__id = species_id
        self.__agents = [agent, ]
        self.__gens_since_imp = gens_since_imp
        self.__avg_fitness = avg_fitness
        self.__size = 1
        self.__allowed_offspring = 0

    # Public Methods
    def add(self, agent):

        """ Adds an agent to the species """

        self.agents.append(agent)
        self.__size += 1

    def filter_parents(self, config):

        """ Returns a list of agents from the species with fitness
            in the top config.parent_proportion of agents """

        sorted_agents = sorted(self.agents, key=attrgetter("fitness"))
        parents = []
        for i in range(int((1-config.parent_proportion) * self.size), self.size):
            parents.append(sorted_agents[i])
        return parents
