from Lightpath import *

class SignalInformation(Lightpath):



    def __init__(self,signal_power,path):
        super().__init__(signal_power,path,0)
        self._signal_power = signal_power
        self._noise_power = 0
        self._latency = 0
        self._path = path
        self.Rs = 32.0e9
        self.df = 50.0e9


    @property
    def signal_power(self):
        return self._signal_power


    def set_signal_power(self,signal_power):
        self._signal_power = signal_power

    @property
    def noise_power(self):
        return self._noise_power

    def set_noise_power(self,noise_power):
        self._noise_power = noise_power

    @property
    def latency(self):
        return self._latency


    def set_latency(self,latency):
        self._latency = latency

    @property
    def path(self):
        return self._path


    def set_path(self,path):
        self._path = path


    def add_noise(self,noise):
        self._noise_power += noise

    def add_latency(self,latency):
        self._latency += latency


    def next(self):
        self._path =self._path[1:]


