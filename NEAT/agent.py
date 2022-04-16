from NEAT.node_gene import NodeGene
from NEAT.conn_gene import ConnGene
import random
import numpy
import math


class Agent:

    """ Has the functionality of one neural network. Contains the methods
        for calculating distance from another agent and performing mutation. """

    CONNECTION_ATTEMPTS = 20

    @property
    def node_genes(self):
        return self.__node_genes

    @node_genes.setter
    def node_genes(self, value):
        self.__node_genes = value

    @property
    def conn_genes(self):
        return self.__conn_genes

    @conn_genes.setter
    def conn_genes(self, value):
        self.__conn_genes = value

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, value):
        self.__fitness = value

    @property
    def adj_fitness(self):
        return self.__adj_fitness

    @adj_fitness.setter
    def adj_fitness(self, value):
        self.__adj_fitness = value

    @property
    def species_id(self):
        return self.__species_id

    @species_id.setter
    def species_id(self, value):
        self.__species_id = value

    def __init__(self):
        self.__node_genes = []
        self.__conn_genes = []
        self.__fitness = 0
        self.__adj_fitness = 0
        self.__species_id = -1

    # Public Methods
    def create_basic_network(self, config, innov):
        self.__create_node_genes(config)
        self.__create_conn_genes(config, innov)

    def get_distance(self, being_compared, distance_threshold, config):

        """ Calls the methods which return the variables in the distance equation.
            Returns the distance between self and being_compared. """

        if len(self.conn_genes) == 0 or len(being_compared.conn_genes) == 0:
            return distance_threshold + 1
        disjoint = self.__get_disjoint(being_compared)
        excess = self.__get_excess(being_compared)
        mean_weight_diff = self.__get_mean_weight_diff(being_compared)
        largest_node_count = self.__get_largest_node_count(being_compared)
        distance = (config.c1 * disjoint) / largest_node_count +\
                   (config.c2 * excess) / largest_node_count +\
                   (config.c3 * mean_weight_diff)
        return distance

    def evaluate(self, inputs):

        """ Calls the methods which feed the inputs through self.
            Returns the outputs of self"""

        self.__load_inputs(inputs)
        self.__propagate()
        return self.__get_outputs()

    def mutate(self, config, innov):

        """ Mutates self by calling the mutation methods. """

        if random.random() < config.add_node_prob and len(self.conn_genes) != 0:
            self.__add_node(innov)
            self.__adjust_layers()
        if random.random() < config.add_conn_prob:
            self.__add_connection(config, innov)
        self.__mutate_conn_weights(config)
        self.__enable_conns(config)

    # Private Methods
    def __create_node_genes(self, config):

        """ Adds NodeGenes to self.node_genes based on the config network parameters. """

        num_nodes = 1 + config.num_inputs + config.num_hidden + config.num_outputs
        if config.num_hidden != 0:
            output_layer = 2
        else:
            output_layer = 1
        for i in range(0, num_nodes):
            if i < 1:
                self.node_genes.append(NodeGene(i, 'b', 0))
            elif i < 1 + config.num_inputs:
                self.node_genes.append(NodeGene(i, 'i', 0))
            elif i < 1 + config.num_inputs + config.num_hidden:
                self.node_genes.append(NodeGene(i, 'h', 1))
            elif i < num_nodes:
                self.node_genes.append(NodeGene(i, 'o', output_layer))

    def __create_conn_genes(self, config, innov):

        """ Adds ConnGenes to self.conn_genes based on the config network parameters. """

        for node_from in self.node_genes:
            if node_from.type != 'o':
                for node_to in self.node_genes:
                    if node_to.layer == node_from.layer + 1:
                        if random.random() <= config.prob_connected:
                            innov_num = innov.get_innov(node_from.id, node_to.id)
                            weight = numpy.random.normal(config.weight_mean, config.weight_std)
                            if weight > config.max_weight:
                                weight = config.max_weight
                            elif weight < config.min_weight:
                                weight = config.min_weight
                            self.conn_genes.append(ConnGene(node_from.id, node_to.id, weight, innov_num))

    def __get_disjoint(self, being_compared):

        """ Returns the number of disjoint connections between self and being_compared. """

        disjoint = 0
        max_innov_agent = max(conn.innov for conn in self.conn_genes)
        max_innov_bc = max(conn.innov for conn in being_compared.conn_genes)
        if max_innov_agent > max_innov_bc:
            smaller_innov = max_innov_bc
        else:
            smaller_innov = max_innov_agent
        for i in range(1, smaller_innov + 1):
            agent_contains_innov = i in (conn.innov for conn in self.conn_genes)
            bc_contains_innov = i in (conn.innov for conn in being_compared.conn_genes)
            if agent_contains_innov ^ bc_contains_innov:
                disjoint += 1
        return disjoint

    def __get_excess(self, being_compared):

        """ Returns the number of excess connections between self and being compared. """

        excess = 0
        self_innov_nums = [conn.innov for conn in self.conn_genes]
        bc_innov_nums = [conn.innov for conn in being_compared.conn_genes]
        max_innov_self = max(self_innov_nums)
        max_innov_bc = max(bc_innov_nums)
        if max_innov_self > max_innov_bc:
            for innov in self_innov_nums:
                if innov > max_innov_bc:
                    excess += 1
        elif max_innov_bc > max_innov_self:
            for innov in bc_innov_nums:
                if innov > max_innov_self:
                    excess += 1
        return excess

    def __get_mean_weight_diff(self, being_compared):

        """ Returns the mean weight difference between self and being compared. """

        sum_weight_diff = 0
        num_matching = 0
        for conn in self.conn_genes:
            bc_weight = next((bc_conn.weight for bc_conn in being_compared.conn_genes
                              if conn.innov == bc_conn.innov), None)
            if bc_weight is not None:
                sum_weight_diff += abs(conn.weight - bc_weight)
                num_matching += 1
        if num_matching > 0:
            return sum_weight_diff / num_matching
        else:
            return 0

    def __get_largest_node_count(self, being_compared):

        """ Returns the number of nodes in the agent with more nodes out of
            self and being_compared. """

        if len(self.node_genes) >= len(being_compared.node_genes):
            return len(self.node_genes)
        else:
            return len(being_compared.node_genes)

    def __load_inputs(self, inputs):

        """ Loads the inputs into the outputs of the input nodes in self. """

        self.node_genes[0].output_value = 1.0
        for i in range(0, len(inputs)):
            self.node_genes[i + 1].output_value = inputs[i]

    def __propagate(self):

        """ Propagates the inputs through self. """

        last_layer = max(node.layer for node in self.node_genes)
        for layer in range(1, last_layer + 1):
            for term_node in self.node_genes:
                if term_node.layer == layer:
                    sum_inputs = 0
                    for conn in self.conn_genes:
                        if conn.output == term_node.id and conn.enabled:
                            sum_inputs += conn.weight * self.node_genes[conn.input].output_value
                    term_node.input_value = sum_inputs
                    term_node.output_value = self.__steepend_sigmoid(sum_inputs)

    @staticmethod
    def __steepend_sigmoid(x):

        """ Returns the result of applying a steepend sigmoid function on x. """

        return 1 / (1 + math.exp(-4.9 * x))

    def __get_outputs(self):

        """ Returns the output of output nodes of self. """

        outputs = [node.output_value for node in self.node_genes if node.type == 'o']
        return outputs

    def __add_node(self, innov):

        """ Mutates self by adding a node to self.node_genes """

        conn = random.choice(self.conn_genes)
        conn.enabled = False
        new_node_id = len(self.node_genes)
        self.node_genes.append(NodeGene(new_node_id, 'h', self.node_genes[conn.output].layer))
        innov_num = innov.get_innov(conn.input, new_node_id)
        self.conn_genes.append(ConnGene(conn.input, new_node_id, conn.weight, innov_num, True))
        innov_num = innov.get_innov(new_node_id, conn.output)
        self.conn_genes.append(ConnGene(new_node_id, conn.output, 1, innov_num, True))

    def __adjust_layers(self):

        """ Adjusts the layer of each node in self.node_genes. """

        for node in self.node_genes:
            node.layer = self.__len_longest_path(node)

    def __len_longest_path(self, node):

        """ Recursive algorithm which returns the longest path to the first layer
            of the neural network from the passed in node. """

        length = 0
        if node.type == 'i' or node.type == 'b':
            return length
        else:
            for conn in self.conn_genes:
                if conn.output == node.id:
                    new_length = self.__len_longest_path(self.node_genes[conn.input]) + 1
                    if new_length > length:
                        length = new_length
            return length

    def __add_connection(self, config, innov):

        """ Mutates self by adding a connection to self.conn_genes between two nodes
            in self.node_genes. """

        num_attempted = 0
        complete = False
        num_layers = max(node.layer for node in self.node_genes)
        while not complete and num_attempted < 20:
            num_attempted += 1
            lower_node = random.choice([node for node in self.node_genes if node.layer < num_layers])
            higher_node = random.choice([node for node in self.node_genes if node.layer > lower_node.layer])
            possible_innov = innov.check_innov(lower_node.id, higher_node.id)
            if not (possible_innov in [conn.innov for conn in self.conn_genes]):
                innov_num = innov.get_innov(lower_node.id, higher_node.id)
                weight = numpy.random.normal(config.weight_mean, config.weight_std)
                if weight > config.max_weight:
                    weight = config.max_weight
                elif weight < config.min_weight:
                    weight = config.min_weight
                self.conn_genes.append(ConnGene(lower_node.id, higher_node.id, weight, innov_num, True))
                complete = True

    def __mutate_conn_weights(self, config):

        """ Randomly mutates the weights of the connections in self.conn_genes. """

        for conn in self.conn_genes:
            if random.random() < config.mutate_weight_prob:
                if random.random() < config.weight_addition_prob:
                    if random.random() < 0.5:
                        if conn.weight > config.max_weight - config.weight_mutate_addition:
                            conn.weight = config.max_weight
                        else:
                            conn.weight += config.weight_mutate_addition
                    else:
                        if conn.weight < config.min_weight + config.weight_mutate_addition:
                            conn.weight = config.min_weight
                        else:
                            conn.weight -= config.weight_mutate_addition
                else:
                    conn.weight = numpy.random.normal(config.weight_mean, config.weight_std)
                    if conn.weight > config.max_weight:
                        conn.weight = config.max_weight
                    elif conn.weight < config.min_weight:
                        conn.weight = config.min_weight

    def __enable_conns(self, config):

        """ Randomly enables disabled connections in self.conn_genes. """

        for conn in self.conn_genes:
            if not conn.enabled:
                if random.random() < config.conn_enable_prob:
                    conn.enabled = True
