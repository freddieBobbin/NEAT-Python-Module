class NodeGene:

    """ User defined data structure which stores the attributes of a node. """

    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type

    @property
    def layer(self):
        return self.__layer

    @layer.setter
    def layer(self, value):
        self.__layer = value

    @property
    def input_value(self):
        return self.__input_value

    @input_value.setter
    def input_value(self, value):
        self.__input_value = value

    @property
    def output_value(self):
        return self.__output_value

    @output_value.setter
    def output_value(self, value):
        self.__output_value = value

    def __init__(self, node_id, node_type, layer):
        self.__id = node_id
        self.__type = node_type
        self.__layer = layer
        self.__input_value = 0
        self.__output_value = 0



