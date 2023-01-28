import matplotlib.pyplot as plt

from Network import Network
from random import shuffle
import numpy as np
import copy
from Connection import Connection


def main():


    network = Network('../Resources/263697.json')

    node_labels = list(network.nodes.keys())


    #100 random connections
    connections = []

    for i in range(100):
        shuffle(node_labels)
        connection = Connection(node_labels[0],node_labels[-1],1e-3)
        connections.append(connection)

    connections1 = copy.deepcopy(connections)

    bins = np.linspace(90,700,20)

    streamed_connections = network.stream(connections1)
    latencies = [connection.latency for connection in streamed_connections]
    latencies_ = np.ma.masked_equal(latencies,0)
    plt.hist(latencies_, bins=25)
    plt.title('Latency Distribution')
    plt.savefig('../Results/LatencyDistribution.png')
    plt.show()

    streamed_connections = network.stream(connections1)
    snrs = [connection.snr for connection in streamed_connections]
    plt.hist(np.ma.masked_equal(snrs, 0), bins=20)
    plt.title('SNR Dstribution')
    plt.savefig('../Results/SNRDistribution.png')
    plt.show()

    latencies = [connection.latency for connection in streamed_connections]
    #total capacity
    print("Average Latency: ", np.average(np.ma.masked_equal(latencies, 0)))
    print("Average SNR: ", np.average(np.ma.masked_equal(snrs, 0)))


if __name__ == '__main__':
    main()