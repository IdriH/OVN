from Line import Line
class Node:



    def __init__(self,input_dictionary):
        self._label = input_dictionary['label']
        self._position = input_dictionary['position']
        self._connected_nodes = input_dictionary['connected_nodes']
        self._successive = {}
        self._transceiver = ''


    @property
    def transciever(self):
        return self._transceiver
    @transciever.setter
    def transciever(self,value):
        self._transceiver = value
    @property
    def get_node_label(self):
        return self._label

    def set_label(self,label):
        self._label = label

    @property
    def get_node_position(self):
        return self._position

    def set_position(self,position):
        self._position = position

    @property
    def get_connected_nodes(self):
        return self._connected_nodes

    def set_connected_nodes(self,connected_nodes):
        self.connected_nodes = connected_nodes

    @property
    def get_successive(self):
        return  self._successive


    def set_successive(self,successive):
        self._successive = successive

    def propagate(self,lightpath,occupation = False):
        path = lightpath.path
        if len(path)>1:
            line_label = path[0] + path[1] # node to node
            line = self._successive[line_label]
            lightpath.next()
            signal_information = line.propagate(lightpath,occupation)
        return lightpath

