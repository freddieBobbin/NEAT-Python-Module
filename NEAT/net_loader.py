from NEAT.agent import Agent
from NEAT.conn_gene import ConnGene
from NEAT.node_gene import NodeGene
import re


class NetLoader:

    """ Contains the methods for loading an agent stored as a text file
        into an Agent object """

    # Public Methods
    @staticmethod
    def load_net(filename):

        """ Loads the file specified by the passed filename into an Agent """

        try:
            file = open(filename, 'r')
        except FileNotFoundError:
            raise FileNotFoundError(f"No such file or directory: {filename}") from None

        agent = Agent()
        conn_list, node_list = NetLoader.__parse_file(file)
        agent.conn_genes = NetLoader.__create_conn_genes(conn_list)
        agent.node_genes = NetLoader.__create_node_genes(node_list)
        return agent

    # Private Methods
    @staticmethod
    def __parse_file(file):

        """ Reads the file and returns two lists containing ConnGene and
            NodeGene attributes as strings """

        lines = file.read().splitlines()
        if len(lines) < 4:
            raise Exception("Invalid file format")

        conn_list = []
        node_list = []
        done_conns = False
        for line in lines:
            if line == '' and not done_conns:
                done_conns = True
                continue
            if not done_conns:
                NetLoader.__check_conn_line(line)
                conn_list.append((line.rstrip(',')).split(','))
            else:
                NetLoader.__check_node_line(line)
                node_list.append((line.rstrip(',')).split(','))
        return conn_list, node_list

    @staticmethod
    def __check_conn_line(line):
        pattern = re.compile(r"[0-9]+,[0-9]+,-*[0-9]+\.[0-9]+,[1-9][0-9]*,((True)|(False)),")
        if pattern.match(line):
            return
        else:
            print(line)
            raise Exception("Invalid file format")

    @staticmethod
    def __check_node_line(line):
        pattern = re.compile(r"[0-9]+,[biho],[0-9]+,")
        if pattern.match(line):
            return
        else:
            raise Exception("Invalid file format")

    @staticmethod
    def __create_conn_genes(conn_list):

        """ Returns the conn_genes list for the loaded agent """

        conn_genes = []
        for conn in conn_list:
            conn_genes.append(ConnGene(int(conn[0]),
                                       int(conn[1]),
                                       float(conn[2]),
                                       int(conn[3]),
                                       conn[4] == "True"))
        return conn_genes

    @staticmethod
    def __create_node_genes(node_list):

        """ Returns the node_genes list for the loaded agent"""

        node_genes = []
        for node in node_list:
            node_genes.append(NodeGene(int(node[0]),
                                       node[1],
                                       int(node[2])))
        return node_genes
