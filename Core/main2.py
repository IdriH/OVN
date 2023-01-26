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

    sat_percent = 70
    # fixed rate --------------------
    network = Network('263697.json')
    n_node = len(network.nodes.keys())
    saturationFix = []
    MsFix = []
    M = 1
    while 1:
        t_mtx = np.ones((n_node,n_node)) * 100 * M

        for i in range(n_node): # diagonal
            t_mtx[i][i] = 0
        elements = list(itertools.permutations(network.nodes.keys(),2))
        #tuples
        n_elem = len(elements)
        for e in elements:      #diagonal
            if e[0] == e[1]:
                elements.remove(e)
        for i in range(100):
            if len(elements) == 0:
                break
            el = random.choice(elements)
            val = network.update_traffic_matrix(t_mtx,el[0],el[1])
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
        network.free_space()
    print(MsFix)
    plt.plot(MsFix,saturationFix)
    plt.title('Saturation Fixed-Rate')
    plt.savefig('Plots/M_fixed_rate.png')
    plt.xlabel('M')
    plt.ylabel('% of unsatisfied requests')
    plt.grid(linestyle='-', linewidth=0.5)
    plt.draw()
