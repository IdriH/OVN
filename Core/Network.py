import json
import numpy as np
from Line import Line
from Node import Node
import matplotlib.pyplot as plt
from SignalInformation import SignalInformation


class Network:

    def __init__(self,nodes_file):
        self._nodes = {}
        self._lines = {}

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


    def propagate(self,signal_information):


        path = signal_information._path
        # for i in range(1,len(path)):
        #     node_1 = self._nodes[path[i]]
        #
        #     line_1 = self._nodes[path[i-1]].get_node_label + self._nodes[path[i]].get_node_label
        #
        #print(self._nodes[path[0]].get_node_label)
        sig_info = self._nodes[path[0]].propagate(signal_information)

        return sig_info

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









