import json
import numpy as np

from Core.Lightpath import Lightpath
from Line import Line
from Node import Node
import matplotlib.pyplot as plt
import pandas as pd
from SignalInformation import SignalInformation
from spicy import special as math
from Connection import Connection


BER_t = 1e-3
Bn = 12.5e9 #noise bandwidth

class Network:

    def __init__(self,nodes_file, transciever = 'fixed_rate'):
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
            if 'transciever' not in node_json[node_label].keys():
                node.transciever = transciever
            else:
                node.transciever = node_json[node_label]['transceiver']

            for connected_node_label in node_dict['connected_nodes']:
                line_dict = {}
                line_label = node_label + connected_node_label
                line_dict['label'] = line_label
                node_position = np.array(node_json[node_label]['position'],dtype = 'float64')
                connected_node_position = np.array(node_json[connected_node_label]['position'],dtype = 'float64')
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
                """
                if pair in self.lines.keys():
                    line = self.lines[pair]
                    signal_power = line.optimized_launch_power(line.eta_nli(signal_information.df, signal_information.Rs))
                signal_information.set_signal_power(signal_power)
                """
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

    def find_best_snr(self, in_node, out_node):
        available_path = self.available_paths(in_node, out_node)
        if available_path:
            inout_df = self.weighted_paths.loc[
                self.weighted_paths.path.isin(available_path)]
            best_snr = np.max(inout_df.snr.values)
            best_path = inout_df.loc[
                inout_df.snr == best_snr].path.values[0]
        else:
            best_path = None
        return best_path

    def find_best_latency(self, in_node, out_node):
        available_path = self.available_paths(in_node, out_node)
        if available_path:
            inout_df = self.weighted_paths.loc[
                self.weighted_paths.path.isin(available_path)]
            best_latency = np.min(inout_df.latency.values)
            best_path = inout_df.loc[
                inout_df.latency == best_latency].path.values[0]
        else:
            best_path = None
        return best_path


    """

    def  find_best_snr(self,node_a,node_b):
        available_paths = self.available_paths(node_a,node_b)
        if self._connected == True:
            ws = self.weighted_paths.sort_values(by = 'snr',ascending=False)

        for path in ws['path']:
            if path[0] == node_a and path[-1] == node_b:
                best_path = path
                if best_path in available_paths:
                    return best_path


        return None

    def find_best_latency(self,node_a,node_b):
        available_paths = self.available_paths(node_a,node_b)
        if self._connected == True:
            ws = self.weighted_paths.sort_values(by = 'latency')

        for path in ws['path']:


            if path[0] == node_a and path[-1] == node_b:
                best_path = path
                if best_path in available_paths:
                    print(best_path)
                    return best_path
    """
    def stream(self,connections,best = 'latency'):
        streamed_connections = []
        for connection in connections:
            input_node = connection.input
            output_node = connection.output
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


                channel = [i for i in range(len(path_occupancy)) if path_occupancy[i] == 'free'][0]

                lightpath = Lightpath(signal_power,path,channel)

                rb = self.calculate_bit_rate(lightpath,self.nodes[input_node].transciever)
                if rb == 0:
                    continue
                else:
                    connection.bit_rate = rb
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

    def calculate_bit_rate(self,lightpath,strategy):
        global BER_t
        global Bn
        Rs = lightpath.Rs
        path = lightpath.path
        Rb = 0
        GSNR_db = pd.array(self.weighted_paths.loc[self.weighted_paths['path'] == path]['snr'])[0]
        GSNR = 10 ** (GSNR_db/10)



        if strategy == 'fixed_rate':
            if GSNR > 2 * math.erfcinv(2*BER_t) ** 2 * (Rs/Bn):
                Rb = 100
            else:
                Rb = 0
        if strategy == 'flex_rate':
            if GSNR < 2 *math.erfcinv(2*BER_t) ** 2 * (Rs/Bn):
                Rb = 0
            elif (GSNR > 2 * math.erfcinv(2*BER_t) ** 2 * (Rs/Bn)) & (GSNR < (14/3)*math.erfcinv((3/2)*BER_t)**2*(Rs/Bn)):
                Rb = 100

            elif (GSNR > (14 / 3) * math.erfcinv((3 / 2) * BER_t) ** 2 * (Rs / Bn)) & (GSNR < 10 * math.erfcinv(
                    (8 / 3) * BER_t) ** 2 * (Rs / Bn)):
                Rb = 200
            elif GSNR > 10 * math.erfcinv((8 / 3) * BER_t) ** 2 * (Rs / Bn):
                Rb = 400

        if strategy == 'shannon':
            Rb = 2*Rs*np.log2(1+Bn/Rs * GSNR) /1e9
        return Rb


    def node_to_number(self,str):
        nodes = list(self.nodes.keys())
        nodes.sort()
        return nodes.index(str)

    def update_traffic_matrix(self,traffic_matrix,nodeA,nodeB):
        A = self.node_to_number(nodeA)
        B = self.node_to_number(nodeB)
        connection = Connection(nodeA,nodeB,1e-3)
        list_con = [connection]
        self.stream(list_con)
        btr = connection.bit_rate
        if btr == 0:
            traffic_matrix[A][B] = float('inf')
            return float('inf')
        traffic_matrix[A][B] -= btr
        return traffic_matrix[A][B]

    def free_space(self):
        states = ['free'] * len(self.route_space['path'])
        for l in self.lines.values():
            l.free_state()
        for i in range(10):
            self.route_space[str(i)] = states