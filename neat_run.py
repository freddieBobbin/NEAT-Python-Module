from NEAT.agent import Agent
from NEAT.innov import Innov
from NEAT.species import Species
from NEAT.selector import Selector
from operator import attrgetter
import random
import copy


class NeatRun:

    """ Contains the methods for the 5 stages of the NEAT algorithm. """

    @property
    def population(self):
        return self.__population

    @property
    def species(self):
        return self.__species

    @property
    def config(self):
        return self.__config

    @property
    def distance_threshold(self):
        return self.__distance_threshold

    @property
    def gen_num(self):
        return self.__gen_num

    def __init__(self, config):
        self.__population = []
        self.__species = []
        self.__config = config
        self.__distance_threshold = self.config.distance_threshold
        self.__innov = Innov()
        self.__gen_num = -1
        self.__create_population()

    # Public Methods
    def generation(self, fitness):

        """ Runs one generation """

        self.__gen_num += 1
        if self.__gen_num != 0:
            self.__calc_allowed_offspring()
            self.__reproduce()
            self.__mutate_agents()
        fitness(self.population)
        self.__speciate(self.__gen_num)

    def get_fittest_agent(self):

        """ Returns the fittest agent in the population. """

        return max(self.population, key=attrgetter("fitness"))

    # Private Methods
    def __create_population(self):

        """ Initialises the population array with new basic agents. """

        self.__population = []
        for i in range(0, self.config.pop_size):
            self.population.append(Agent())
            self.__population[i].create_basic_network(self.config, self.__innov)

    def __speciate(self, gen_num):

        """ Places population agents into species. """

        temp_species = copy.deepcopy(self.species)
        self.__species = []
        if gen_num == 0:
            self.__speciate_without_reps()
        else:
            self.__speciate_with_reps(temp_species)
            if sum(specie.size for specie in self.species) != self.config.pop_size:
                self.__speciate_without_reps()
        self.__adjust_dist_threshold()

    def __find_reps(self, temp_species):

        """ Returns a list of agents which represent each specie in the previous
            generation. Re-initialises each species from the previous generation
            which had offspring. """

        id_counter = 0
        reps = []
        for specie in temp_species:
            current_agents = [agent for agent in self.population if agent.species_id == specie.id]
            if len(current_agents) != 0:
                rep = max(current_agents, key=attrgetter("fitness"))
                reps.append(rep)
                self.species.append(Species(id_counter, rep, specie.avg_fitness, specie.gens_since_imp))
                rep.species_id = id_counter
                id_counter += 1
        return reps

    def __speciate_with_reps(self, temp_species):

        """ Speciates the population using representatives of the previous
            generation's species. """

        reps = self.__find_reps(temp_species)
        for agent in self.population:
            if agent not in reps:
                agent.species_id = -1
        for rep in reps:
            for being_compared in self.population:
                if being_compared.species_id == -1:
                    distance = rep.get_distance(being_compared, self.distance_threshold, self.config)
                    if distance < self.distance_threshold:
                        self.species[rep.species_id].add(being_compared)
                        being_compared.species_id = rep.species_id

    def __speciate_without_reps(self):

        """ Speciates agents from the population without using representatives. """

        id_counter = len(self.species)
        for agent in self.population:
            if agent.species_id == -1:
                agent.species_id = id_counter
                self.species.append(Species(id_counter, agent))
                for being_compared in self.population:
                    if being_compared.species_id == -1:
                        distance = agent.get_distance(being_compared, self.distance_threshold, self.config)
                        if distance < self.distance_threshold:
                            self.species[agent.species_id].add(being_compared)
                            being_compared.species_id = agent.species_id
                id_counter += 1

    def __adjust_dist_threshold(self):

        """ Adjusts the distance threshold depending on whether the observed number of species
            is greater than or less than the target number of species. """

        if len(self.species) < self.config.target_species_num:
            if self.distance_threshold > 2*self.config.distance_threshold_adjustment:
                self.__distance_threshold -= self.config.distance_threshold_adjustment
        elif len(self.species) > self.config.target_species_num:
            self.__distance_threshold += self.config.distance_threshold_adjustment

    def __calc_allowed_offspring(self):

        """ Calculates the number of offspring each species is allowed to have. """

        sum_adj_fitness = 0
        for agent in self.population:
            agent.adj_fitness = agent.fitness / self.species[agent.species_id].size
            sum_adj_fitness += agent.adj_fitness
        pop_avg_adj_fitness = sum_adj_fitness / self.config.pop_size

        for specie in self.species:
            pre_avg_fitness = specie.avg_fitness
            specie.avg_fitness = 0
            for agent in specie.agents:
                specie.avg_fitness += agent.adj_fitness
            if specie.avg_fitness <= pre_avg_fitness:
                specie.gens_since_imp += 1
            else:
                specie.gens_since_imp = 0
            if specie.gens_since_imp <= self.config.stagnation_threshold:
                specie.allowed_offspring = specie.avg_fitness / pop_avg_adj_fitness
            else:
                specie.allowed_offspring = 0
        self.__round_allowed_offspring()

    def __round_allowed_offspring(self):

        """ Rounds the allowed number of offspring for each species to an
            integer, whilst preserving the total allowed offspring for the population. """

        rest = 0
        total = 0
        for specie in self.species:
            new_value = round(specie.allowed_offspring + rest)
            rest += specie.allowed_offspring - new_value
            specie.allowed_offspring = new_value
            total += new_value

    def __reproduce(self):

        """ Calls the method which implements elitism if elitism is enabled.
            Breeds each specie in the population. """

        if self.config.elitism:
            self.__preserve_elite()
            pop_index = 0
        else:
            self.__create_population()
            pop_index = -1
        for specie in self.species:
            pop_index = self.__breed_specie(specie, pop_index)

    def __preserve_elite(self):

        """ Copies the fittest agent from the current generation to the next generation. """

        fittest_agent = self.get_fittest_agent()
        self.__create_population()
        if self.species[fittest_agent.species_id].allowed_offspring > 0:
            self.population[0] = fittest_agent
            self.species[fittest_agent.species_id].allowed_offspring -= 1

    def __breed_specie(self, specie, pop_index):

        """ Creates a list of the available parents for the passed species and
            chooses parents to crossover."""

        parents = specie.filter_parents(self.__config)
        selector = Selector(parents)
        for i in range(specie.allowed_offspring):
            pop_index += 1
            p1 = selector.sto_acc()
            p2 = selector.sto_acc()
            self.__crossover(p1, p2, pop_index)
        return pop_index

    def __crossover(self, p1, p2, pop_index):

        """ Performs crossover of two agents. The offspring is created
            for the next generation in the population list. """

        if p1.fitness > p2.fitness:
            self.population[pop_index].conn_genes = copy.deepcopy(p1.conn_genes)
            self.population[pop_index].node_genes = copy.deepcopy(p1.node_genes)
        elif p1.fitness < p2.fitness:
            self.population[pop_index].conn_genes = copy.deepcopy(p2.conn_genes)
            self.population[pop_index].node_genes = copy.deepcopy(p2.node_genes)
        else:
            if random.random() < 0.5:
                self.population[pop_index].conn_genes = copy.deepcopy(p1.conn_genes)
                self.population[pop_index].node_genes = copy.deepcopy(p1.node_genes)
            else:
                self.population[pop_index].conn_genes = copy.deepcopy(p2.conn_genes)
                self.population[pop_index].node_genes = copy.deepcopy(p2.node_genes)
        self.population[pop_index].species_id = p1.species_id

        for conn1 in p1.conn_genes:
            if conn1.innov in (conn2.innov for conn2 in p2.conn_genes):
                os_conn = next(conn_os for conn_os in self.population[pop_index].conn_genes
                               if conn_os.innov == conn1.innov)
                if random.random() < 0.5:
                    os_conn.weight = conn1.weight
                else:
                    os_conn.weight = next(conn2 for conn2 in p2.conn_genes if conn2.innov == conn1.innov).weight

    def __mutate_agents(self):

        """ Calls the method responsible for mutation of each agent in the
            population list. """

        if self.config.elitism:
            for agent in self.population[1:]:
                agent.mutate(self.config, self.__innov)
        else:
            for agent in self.population:
                agent.mutate(self.config, self.__innov)
