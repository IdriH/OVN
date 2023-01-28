import matplotlib.pyplot as plt

from Network import Network
from random import shuffle
import numpy as np
import copy
from Connection import Connection

#this main is used for simulating 100 random connections using all transciever technologies


def main():
    network_fixed_rate = Network('../Resources/263697.json')
    network_flex_rate = Network('../Resources/263697.json','flex_rate')
    network_shannon = Network('../Resources/263697.json','shannon')
    node_labels = list(network_fixed_rate.nodes.keys())


#100 random connections
    connections = []

    for i in range(100):
        shuffle(node_labels)
        connection = Connection(node_labels[0],node_labels[-1],1e-3)
        connections.append(connection)

    connections1 = copy.deepcopy(connections)
    connections2 = copy.deepcopy(connections)
    connections3 = copy.deepcopy(connections)
    bins = np.linspace(90,700,20)

    #fixed rate
    streamed_connections_fixed_rate = network_fixed_rate.stream(connections1,best = 'snr')
    snrs = [connection.snr for connection in streamed_connections_fixed_rate]
    snrs_ = np.ma.masked_equal(snrs,0)
    plt.hist(snrs_,bins = 20)

    plt.title('SNR Distribution Full fixed rate ')
    plt.xlabel('dB')
    plt.savefig('../Results/Lab8/8.9/SNRDistributionFullfixed_rate.png')
    plt.show()

    bit_rate_fixed_rate = [connection.bit_rate for connection in streamed_connections_fixed_rate]
    b_r_f_r = np.ma.masked_equal(bit_rate_fixed_rate,0)
    plt.hist(b_r_f_r,bins,label = 'fixed-rate')
    plt.title('BitRate Full fixed-rate')
    plt.xlabel('Gbps')
    plt.savefig('../Results/Lab8/8.9/BitRateFullFixed_rate.png')
    plt.show()

    # flex_rate
    streamed_connections_flex_rate = network_flex_rate.stream(connections2,best = 'snr')
    snrs = [connection.snr for connection in streamed_connections_flex_rate]
    snrs_ = np.ma.masked_equal(snrs,0)

    plt.hist(snrs_,bins = 20)
    plt.title('SNR Distribution flex-rate')
    plt.xlabel('dB')
    plt.savefig('../Results/Lab8/8.9/SNRDistributionFullflex_rate.png')
    plt.show()

    bit_rate_flex_rate = [connection.bit_rate for connection in streamed_connections_flex_rate]
    brfr = np.ma.masked_equal(bit_rate_flex_rate,0)
    plt.hist(brfr,bins,label = 'flex_rate')

    plt.xlabel('Gbps')
    plt.title('BitRate Full Flex-Rate')
    plt.savefig('../Results/Lab8/8.9/BitRateFullFlex_Rate.png')
    plt.show()

    #shanon
    streamed_connections_shannon = network_shannon.stream(connections3, best='snr')

    snrs = [connection.snr for connection in streamed_connections_shannon]
    snrs_ = np.ma.masked_equal(snrs, 0)
    plt.hist(snrs_, bins=20)

    plt.title('SNR Distribution Full Shannon')
    plt.xlabel('dB')
    plt.savefig('../Results/Lab8/8.9/SNRDistributionFullshannon.png')
    #plt.show()

    bit_rate_shannon = [connection.bit_rate for connection in streamed_connections_shannon]
    brs = np.ma.masked_equal(bit_rate_shannon, 0)

    plt.hist(brs, bins, label='shannon')

    plt.xlabel('Gbps')
    plt.title('BitRate Full Shannon')
    plt.savefig('../Results/Lab8/8.9/BitRateFullShannon.png')

    plt.show()


##########
    """
    streamed_connections = network.stream(connections)
    latencies = [connection.latency for connection in streamed_connections]
    latencies_ = np.ma.masked_equal(latencies,0)
    plt.hist(latencies_, bins=25)
    plt.title('Latency Distribution')
    plt.savefig('../Results/LatencyDistribution.png')
    plt.show()
    """
    #streamed_connections = network.stream(connections)
    #snrs = [connection.snr for connection in streamed_connections]
    #plt.hist(np.ma.masked_equal(snrs, 0), bins=20)
    #plt.title('SNR Dstribution')
    #plt.savefig('../Results/SNRDistribution.png')
    #plt.show()

    #latencies = [connection.latency for connection in streamed_connections]
    #total capacity
    #print("Average Latency: ", np.average(np.ma.masked_equal(latencies, None)))
    #print("Average SNR: ", np.average(np.ma.masked_equal(snrs, 0)))

    sourceFile = open('../Results/Lab8/8.9/Capacity results','w')
    print("Total Capacity Fixed-Rate:", np.sum(bit_rate_fixed_rate),file = sourceFile)
    print("Average Capacity Fixed-Rate:", np.mean(np.ma.masked_equal(bit_rate_fixed_rate, 0)),file = sourceFile)
    print("Total Capacity Flex-Rate:", np.sum(bit_rate_flex_rate),file = sourceFile)
    print("Average Capacity Flex-Rate:", np.mean(np.ma.masked_equal(bit_rate_flex_rate, 0)),file = sourceFile)
    print("Total Capacity Shannon:", np.sum(bit_rate_shannon).round(2),file = sourceFile)
    print("Average Capacity Shannon:", np.mean(np.ma.masked_equal(bit_rate_shannon, 0).round(2)),file = sourceFile)



if __name__ == "__main__":
    main()
