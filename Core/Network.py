import json
import numpy as np

from Core.Lightpath import Lightpath
from Line import Line
from Node import Node
import matplotlib.pyplot as plt
import pandas as pd
from SignalInformation import SignalInformation


class Network:

    def __init__(self,nodes_file):
        self._nodes = {}
        self._lines = {}
        self._connected = False
        self._weighted_paths = None
        self._route_space = None

        node_json = json.load(open(nodes_file,'r'))

        for node_label in node_json:
            node_dict = node_json[node_label]
            node_dict['label'] = node_label
            node = Node(node_dict)
            self._nodes[node_label] = node

            for connected_node_label in node_dict['connected_nodes']:
                line_dict = {}
                line_label = node_label + connected_node_label
                line_dict['label'] = line_label
                node_position = np.array(node_json[node_label]['position'])
                connected_node_position = np.array(node_json[connected_node_label]['position'])
                line_dict['length'] = np.sqrt(np.sum(node_position-connected_node_position)**2)
                line = Line(line_dict)
                self._lines[line_label] = line

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def connected(self):
        return self._connected

    @property
    def weighted_paths(self):
        return self._weighted_paths

    @property
    def route_space(self):
        return self._route_space

    def connect(self):
        nodes_dict = self._nodes
        lines_dict = self._lines
        for node_label in nodes_dict:
            node = nodes_dict[node_label]
            for connected_node in node.get_connected_nodes:
                line_label = node_label + connected_node
                line = lines_dict[line_label]
                line.successive[connected_node] = nodes_dict[connected_node]
                node._successive[line_label] = lines_dict[line_label]
        self._connected = True
    def find_paths(self,node_a,node_b,path = []):
        path = path + [node_a]

        if node_a == node_b:

            return [path]
        paths = []




        node_ao = self._nodes[node_a]
        connected_nodes = node_ao.get_connected_nodes

        for connected_node in connected_nodes:

            if connected_node not in path:

                subpaths = self.find_paths(connected_node,node_b,path.copy())

                for subpath in subpaths:
                    paths.append(subpath)

        return paths


    def propagate(self,lightpath,occupation = False):


        path = lightpath.path

        # for i in range(1,len(path)):
        #     node_1 = self._nodes[path[i]]
        #
        #     line_1 = self._nodes[path[i-1]].get_node_label + self._nodes[path[i]].get_node_label
        #
        #print(self._nodes[path[0]].get_node_label)

        start_node = self.nodes[path[0]]
        propagated_lightpath = start_node.propagate(lightpath,occupation)

        return propagated_lightpath

    def draw(self):
        nodes = self._nodes
        for node_label in nodes:
            n0 = nodes[node_label]
            x0 = n0.get_node_position[0]
            y0 = n0.get_node_position[1]
            plt.plot(x0, y0, 'g')
            plt.text(x0 + 100, y0 + 100, node_label)
            for connected_node_label in n0.get_connected_nodes:
                n1 = nodes[connected_node_label]
                x1 = n1.get_node_position[0]
                y1 = n1.get_node_position[1]
                plt.plot([x0, x1], [y0, y1], 'b')
        plt.title('Network')
        plt.show()


    @property
    def weighted_paths(self):
        return  self._weighted_paths

    def set_weighted_paths(self, signal_power):
        if not self._connected:
            self.connect()

        node_labels = self._nodes.keys()
        pairs = []
        for label1 in node_labels:
            for label2 in node_labels:
                if label1 != label2:
                    pairs.append(label1 + label2)
        df = pd.DataFrame()
        paths = []
        latencies = []
        noises = []
        snrs = []
        for pair in pairs:
            for path in self.find_paths(pair[0], pair[1]):
                path_string = ''
                for node in path:
                    path_string += node
                paths.append(path_string)
                # Propagation
                signal_information = SignalInformation(signal_power, path)
                signal_information = self.propagate(signal_information,occupation = False)
                latencies.append(signal_information._latency)
                noises.append(signal_information._noise_power)
                snrs.append(
                    10 * np.log10(
                        signal_information._signal_power /
                        signal_information._noise_power
                        )
                )
        df['path'] = paths
        df['latency'] = latencies
        df['noise' ] = noises
        df['snr' ] = snrs
        self._weighted_paths = df

        route_space = pd.DataFrame()
        route_space['path'] = paths
        for i in range(10):
            route_space[str(i)] = ['free']*len(paths)
        self._route_space =route_space

    def  find_best_snr(self,node_a,node_b):
        available_paths = self.available_paths(node_a,node_b)
        if self._connected == True:
            ws = self.weighted_paths.sort_values(by = 'snr',ascending=False)


        for path in available_paths:
                if path[0] == node_a and path[-1] == node_b:
                    return path


        return None

    def find_best_latency(self,node_a,node_b):
        available_paths = self.available_paths(node_a,node_b)
        if self._connected == True:
            ws = self.weighted_paths.sort_values(by = 'latency')

        for path in available_paths:

                if path[0] == node_a and path[-1] == node_b:
                    return path
        return None

    def stream(self,connections,best = 'latency'):
        streamed_connections = []
        for connection in connections:
            input_node = connection._input_node
            output_node = connection._output_node
            signal_power = connection.signal_power

            if best == 'latency':
                path = self.find_best_latency(input_node,output_node)
            elif best == 'snr':
                path = self.find_best_snr(input_node,output_node)
            else:
                print('Error:best connection not recognized')
                continue
            if path:
                path_occupancy = self.route_space.loc[
                                     self.route_space.path == path].T.values[1:]

                channel = [i for i in range(len(path_occupancy))
                 if path_occupancy[i] == 'free'][0]

                in_lightpath = Lightpath(signal_power, path, channel)
                out_lightpath = self.propagate(in_lightpath, True)
                connection.latency = out_lightpath.latency
                noise_power = out_lightpath.noise_power
                connection.snr = 10 * np.log10(signal_power / noise_power)
                self.update_route_space(path, channel)
            else:
                connection.latency = None
                connection.snr = 0
            streamed_connections.append(connection)
        return  streamed_connections

    def available_paths(self,input_node,output_node):
        if self.weighted_paths is None:
            self.set_weighted_paths(1)
        all_paths = [path for path in self._weighted_paths.path.values
                     if((path[0] == input_node)and (path[-1] == output_node))]
        available_paths = []
        for path in all_paths:
            path_occupancy = self.route_space.loc[
                self.route_space.path == path].T.values[1:]
            if 'free' in path_occupancy:
                available_paths.append(path)
        return  available_paths
    @staticmethod
    def path_to_line_set(path):
        print(path)
        return set([path[i] + path[i+1] for i in range(len(path)-1)])

    def update_route_space(self,path,channel):
        all_paths = [self.path_to_line_set(p) for p in self.route_space.path.values]
        states = self.route_space[str(channel)]
        lines = self.path_to_line_set(path)
        for i in range(len(all_paths)):
            line_set = all_paths[i]
            if lines.intersection(line_set):
                states[i] = 'occupied'
        self.route_space[str(channel)] = states
