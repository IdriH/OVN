import itertools
import random

# this main is used for reporting the results of increasing the matrix traffic
# until network saturation

import pandas as pd
from Network import *
from random import shuffle
import matplotlib.pyplot as plt
import copy

def main():

    sat_percent = 90
    # fixed rate --------------------
    """
    network_fixed_rate = Network('../Resources/263697.json')
    n_node = len(network_fixed_rate.nodes.keys())
    saturationFix = []
    MsFix = []
    M = 1
    while 1:
        t_mtx = np.ones((n_node,n_node)) * 100 * M

        for i in range(n_node): # diagonal
            t_mtx[i][i] = 0
        elements = list(itertools.permutations(network_fixed_rate.nodes.keys(),2))
        #tuples
        n_elem = len(elements)
        for e in elements:      #diagonal
            if e[0] == e[1]:
                elements.remove(e)
        for i in range(120):
            if len(elements) == 0:
                break
            el = random.choice(elements)
            val = network_fixed_rate.update_traffic_matrix(t_mtx,el[0],el[1])
            if (val == 0) | (val == np.inf):
                elements.remove(el)

        sat = 0
        for row in t_mtx:
            for el in row:
                if el == float('inf'):
                        sat+=1
        sat = sat/n_elem * 100
        saturationFix.append(sat)
        MsFix.append(M)
        print(sat,'vs',sat_percent)
        if sat > sat_percent:
            break

        M += 1
        network_fixed_rate.free_space()


    #cutting the most congested link



    plt.plot(MsFix,saturationFix)
    plt.title('Saturation Fixed-Rate')

    plt.xlabel('M')
    plt.ylabel('% of unsatisfied requests')
    plt.grid(linestyle='-', linewidth=0.5)
    plt.savefig('../Results/M_fixed_rate_1_2.png')
    plt.show()

    """
# flex rate_____________________________________________________________________________
    network_flex_rate = Network('../Resources/263697.json', 'flex_rate')
    n_node = len(network_flex_rate.nodes.keys())
    saturationflex = []
    Msflex = []
    M = 1
    while (1):
        t_mtx = np.ones((n_node, n_node)) * 100 * M
        for i in range(n_node):
            t_mtx[i][i] = 0
        elements = list(itertools.permutations(network_flex_rate.nodes.keys(), 2))
        n_elem = len(elements)
        for e in elements:  # remove the diagonal
            if e[0] == e[1]:
                elements.remove(e)
        for i in range(120):
            if len(elements) == 0:
                break
            el = random.choice(elements)
            val = network_flex_rate.update_traffic_matrix(t_mtx, el[0], el[1])
            if (val < 0) | (val == np.inf):
                elements.remove(el)
        sat = 0
        for row in t_mtx:
            for el in row:
                if el == float('inf'):
                    sat += 1
        sat = sat / n_elem * 100
        saturationflex.append(sat)
        Msflex.append(M)
        print(sat, 'vs', sat_percent)
        if sat > sat_percent:
            break
        M += 1
        network_flex_rate.free_space()
    plt.plot(Msflex, saturationflex)
    plt.title('Saturation Flex-Rate')

    plt.xlabel('M')
    plt.ylabel('% of unsatisfied requests')
    plt.grid(linestyle='-', linewidth=0.5)
    plt.draw()
    plt.savefig('../Results/M_flex_rate_2.png')


if __name__ == '__main__':
    main()