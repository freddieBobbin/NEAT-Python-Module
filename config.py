import configparser


class Config:

    """ Contains the methods which use the configparser library to parse
        the config parameters. Each parameter has its own getter. """

    def __init__(self, file_name):
        self.__config = configparser.ConfigParser()
        self.__config.read(file_name)

    # Properties
    # [Run]
    @property
    def fitness_threshold(self):
        try:
            value = float(self.__config.get("Run", "fitness_threshold"))
            return value
        except ValueError:
            raise TypeError("fitness_threshold must be of type float") from None

    # [Population]
    @property
    def pop_size(self):
        try:
            value = int(self.__config.get("Population", "pop_size"))
        except ValueError:
            raise TypeError("pop_size must of type int") from None
        if value > 0:
            return value
        else:
            raise ValueError("pop_size must be at least 1")

    # [NeuralNet]
    @property
    def num_inputs(self):
        try:
            value = int(self.__config.get("NeuralNet", "num_inputs"))
        except ValueError:
            raise TypeError("num_inputs must be of type int") from None
        if value > 0:
            return value
        else:
            raise ValueError("num_inputs must be at least 1")

    @property
    def num_hidden(self):
        try:
            value = int(self.__config.get("NeuralNet", "num_hidden"))
        except ValueError:
            raise TypeError("num_hidden must be of type int") from None
        if value >= 0:
            return value
        else:
            raise ValueError("num_hidden must be greater than or equal to 0")

    @property
    def num_outputs(self):
        try:
            value = int(self.__config.get("NeuralNet", "num_outputs"))
        except ValueError:
            raise TypeError("num_outputs must be of type int") from None
        if value > 0:
            return value
        else:
            raise ValueError("num_outputs must be at least 1")

    @property
    def weight_mean(self):
        try:
            return float(self.__config.get("NeuralNet", "weight_mean"))
        except ValueError:
            raise TypeError("weight_mean must be of type float") from None

    @property
    def weight_std(self):
        try:
            value = float(self.__config.get("NeuralNet", "weight_std"))
        except ValueError:
            raise TypeError("weight_std must be of type float") from None
        if value >= 0:
            return value
        else:
            raise ValueError("weight_std must be greater than or equal to 0")

    @property
    def max_weight(self):
        try:
            return float(self.__config.get("NeuralNet", "max_weight"))
        except ValueError:
            raise TypeError("max_weight must be of type float") from None

    @property
    def min_weight(self):
        try:
            return float(self.__config.get("NeuralNet", "min_weight"))
        except ValueError:
            raise TypeError("min_weight must be of type float") from None

    @property
    def prob_connected(self):
        try:
            value = float(self.__config.get("NeuralNet", "prob_connected"))
        except ValueError:
            raise TypeError("prob_connected must be of type float") from None
        if 0.0 <= value <= 1.0:
            return value
        else:
            raise ValueError("prob_connected must be in range 0.0 - 1.0")

    # [Speciation]
    @property
    def target_species_num(self):
        try:
            value = int(self.__config.get("Speciation", "target_species_num"))
        except ValueError:
            raise TypeError("target_species_num must be of type int") from None
        if 1 <= value <= self.pop_size:
            return value
        else:
            raise ValueError("target_species_num must be at least 1 and less than or equal to pop_size")

    @property
    def distance_threshold(self):
        try:
            value = float(self.__config.get("Speciation", "distance_threshold"))
        except ValueError:
            raise TypeError("distance_threshold must be of type float") from None
        if 0 < value:
            return value
        else:
            raise ValueError("distance_threshold must be greater than 0")

    @property
    def distance_threshold_adjustment(self):
        try:
            value = float(self.__config.get("Speciation", "distance_threshold_adjustment"))
        except ValueError:
            raise TypeError("distance_threshold_adjustment must be of type float") from None
        if value >= 0:
            return value
        else:
            raise ValueError("distance_threshold_adjustment must be greater than or equal to 0")

    @property
    def c1(self):
        try:
            value = float(self.__config.get("Speciation", "c1"))
        except ValueError:
            raise TypeError("c1 must be of type float") from None
        if value >= 0:
            return value
        else:
            raise ValueError("c1 must be greater than or equal to 0")

    @property
    def c2(self):
        try:
            value = float(self.__config.get("Speciation", "c2"))
        except ValueError:
            raise TypeError("c2 must be of type float") from None
        if value >= 0:
            return value
        else:
            raise ValueError("c2 must be greater than or equal to 0")

    @property
    def c3(self):
        try:
            value = float(self.__config.get("Speciation", "c3"))
        except ValueError:
            raise TypeError("c3 must be of type float") from None
        if value >= 0:
            return value
        else:
            raise ValueError("c3 must be greater than or equal to 0")

    # [Crossover]
    @property
    def elitism(self):
        return self.__config.get("Crossover", "elitism") == "True"

    @property
    def stagnation_threshold(self):
        try:
            value = int(self.__config.get("Crossover", "Stagnation_threshold"))
        except ValueError:
            raise TypeError("stagnation_threshold must be of type int") from None
        if value >= 0:
            return value
        else:
            raise ValueError("stagnation_threshold must be greater than or equal to 0")

    @property
    def parent_proportion(self):
        try:
            value = float(self.__config.get("Crossover", "parent_proportion"))
        except ValueError:
            raise TypeError("parent_proportion must be of type float") from None
        if 0.0 < value <= 1.0:
            return value
        else:
            raise ValueError("parent_proportion must be in range 0.0 < p <= 1.0")

    # [Mutation]
    @property
    def add_node_prob(self):
        try:
            value = float(self.__config.get("Mutation", "add_node_prob"))
        except ValueError:
            raise TypeError("add_node_prob must be of type float") from None
        if 0.0 <= value <= 1.0:
            return value
        else:
            raise ValueError("add_node_prob must be in range 0.0 - 1.0")

    @property
    def add_conn_prob(self):
        try:
            value = float(self.__config.get("Mutation", "add_conn_prob"))
        except ValueError:
            raise TypeError("add_conn_prop must be of type float") from None
        if 0.0 <= value <= 1.0:
            return value
        else:
            raise ValueError("add_conn_prob must be in range 0.0 - 1.0")

    @property
    def mutate_weight_prob(self):
        try:
            value = float(self.__config.get("Mutation", "mutate_weight_prob"))
        except ValueError:
            raise TypeError("mutate_weight_prob must be of type float") from None
        if 0.0 <= value <= 1.0:
            return value
        else:
            raise ValueError("mutate_weight_prob must be in range 0.0 - 1.0")

    @property
    def weight_addition_prob(self):
        try:
            value = float(self.__config.get("Mutation", "weight_addition_prob"))
        except ValueError:
            raise TypeError("weight_addition_prob must be of type float") from None
        if 0.0 <= value <= 1.0:
            return value
        else:
            raise ValueError("weight_addition_prob must be in range 0.0 - 1.0")

    @property
    def weight_mutate_addition(self):
        try:
            return float(self.__config.get("Mutation", "weight_mutate_addition"))
        except ValueError:
            raise TypeError("weight_mutate_addition must be of type float") from None

    @property
    def conn_enable_prob(self):
        try:
            value = float(self.__config.get("Mutation", "conn_enable_prob"))
        except ValueError:
            raise TypeError("conn_enable_prob must be of type float") from None
        if 0.0 <= value <= 1.0:
            return value
        else:
            raise ValueError("conn_enable_prob must be in range 0.0 - 1.0")
