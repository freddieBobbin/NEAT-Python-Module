import numpy


class Innov:

    """ Contains the innov look-up and methods which can be used to check and assign
        innovation numbers """

    def __init__(self):
        self.__innov_num = 0
        self.__look_up = numpy.zeros((1000, 1000), dtype=int)

    def get_innov(self, id1, id2):

        """ Returns a new innovation number if no connection has previously
            been created between node with the passed ids. Otherwise, returns
            an innovation number from the look-up table. """

        innov_num = self.check_innov(id1, id2)
        if innov_num == 0:
            self.__innov_num += 1
            self.__look_up[id1][id2] = self.__innov_num
            innov_num = self.__innov_num
        return innov_num

    def check_innov(self, id1, id2):

        """ Returns an innovation number from the look-up"""

        return self.__look_up[id1][id2]
