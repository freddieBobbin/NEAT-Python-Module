class ConnGene:

    """ User defined data structure which stores the attributes of a connection. """

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, value):
        self.__input = value

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):
        self.__output = value

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        self.__weight = value

    @property
    def innov(self):
        return self.__innov

    @innov.setter
    def innov(self, value):
        self.__innov = value

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, value):
        self.__enabled = value

    def __init__(self, input_id, output_id, weight, innov, enabled=True):
        self.__input = input_id
        self.__output = output_id
        self.__weight = weight
        self.__innov = innov
        self.__enabled = enabled
