import matplotlib.pyplot as plt

from Network import Network
from random import shuffle
import numpy as np
import copy
from Connection import Connection
import itertools
import random

#this main is used for simulating 100 random connections using all transciever technologies


def main():
    network_flex_rate = Network('../Resources/263697.json','flex_rate')
    node_labels = list(network_flex_rate.nodes.keys())

    """
    #100 random connections
    connections = []

    for i in range(100):
        shuffle(node_labels)
        connection = Connection(node_labels[0],node_labels[-1],1e-3)
        connections.append(connection)

    connections1 = copy.deepcopy(connections)
    """
    n_node = len(network_flex_rate.nodes.keys())
    t_mtx = np.ones((n_node, n_node)) * 100
    for i in range(n_node):
        t_mtx[i][i] = 0

    #for connection in connections1:  # remove the diagonal
    #    val = network_flex_rate.update_traffic_matrix(t_mtx,connection.input, connection.output)
    elements = list(itertools.permutations(network_flex_rate.nodes.keys(), 2))
    # tuples
    n_elem = len(elements)
    for e in elements:  # diagonal
        if e[0] == e[1]:
            elements.remove(e)
    for i in range(120):
        if len(elements) == 0:
            break
        el = random.choice(elements)
        val = network_flex_rate.update_traffic_matrix(t_mtx, el[0], el[1])
        if (val == 0) | (val == np.inf):
            elements.remove(el)

    #network_flex_rate.strong_failure("AB")


    print(network_flex_rate.logger_df())
    network_flex_rate.logger_df().to_csv("./LOGGERdf.csv")
    print(network_flex_rate.route_space)
    network_flex_rate.route_space.to_csv("./RouteSpace.csv")
    print(t_mtx)


if __name__ == '__main__':
    main()