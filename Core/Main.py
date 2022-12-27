import numpy as np

from Network import Network
from SignalInformation import  SignalInformation
import pandas as pd

network = Network('../Resources/nodes.json')
paths = network.find_paths('A','F',[])
# print(type(paths))

network.connect()

signal_info = SignalInformation(200,paths[1])

sig_update  = network.propagate(signal_info)


network.draw()






