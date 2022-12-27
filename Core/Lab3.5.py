import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.constants import c
from Line import Line
from Node import Node
from SignalInformation import SignalInformation
from Network import Network

network = Network('../Resources/nodes.json')
network.connect()

#Lab 3.5 find snr ,latency,noise power for all possible paths
network_nodes = network._nodes.keys()
pairs = []
for node1 in network_nodes:
    for node2 in network_nodes:
        if node1 != node2:
            pairs.append(node1+node2)

df = pd.DataFrame()
paths = []
latencies = []
noises = []
snrs = []

for pair in pairs:
    for path in network.find_paths(pair[0],pair[1]):
        path_string = ''
        for node in path:
            path_string += node + ' ->'
            paths.append(path_string[:-2])

            signal_information = SignalInformation(1,path)
            signal_information = network.propagate(signal_information)
            latencies.append(signal_information._latency)
            noises.append(signal_information._noise_power)
            snrs.append(10 * np.log10(signal_information._signal_power/signal_information._noise_power))

df['path']  = paths
df['latency'] = latencies
df['noise'] = noises
df['snr'] = snrs

df.to_csv('../Results/paths_info.csv')