#this will act as main
from Connection import Connection
import numpy as np
from Network import Network
from SignalInformation import  SignalInformation
from random import shuffle
import matplotlib.pyplot as plt

network = Network('../Resources/nodes.json')
network.connect()
node_labels = list(network._nodes.keys())
connections = []



for i in range(100):
    shuffle(node_labels)
    connection = Connection(node_labels[0],node_labels[-1],1)
    connections.append(connection)

#LAb5 comment these

# streamed_connections = network.stream(connections)
# latencies = [connection.latency for connection in streamed_connections]
# plt.hist(latencies)
# plt.title('Latency Distribution')
# plt.show()

streamed_connections = network.stream(connections,best = 'snr')
snrs = [connection.snr for connection in streamed_connections]

plt.hist(snrs)
plt.title('SNR distribution')
plt.show()