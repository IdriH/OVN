
class SignalInformation:

    _signal_power = 0
    _noise_power = 0
    _latency = 0

    def __init__(self,signal_power,path):
        self._signal_power = signal_power
        self._noise_power = 0
        self._latency = 0
        self._path = path



    @property
    def get_signal_power(self):
        return self._signal_power


    def set_signal_power(self,signal_power):
        self._signal_power = signal_power

    @property
    def get_noise_power(self):
        return self._noise_power

    def set_noise_power(self,noise_power):
        self._noise_power = noise_power

    @property
    def get_latency(self):
        return self._latency


    def set_latency(self,latency):
        self._latency = latency

    @property
    def get_path(self):
        return self._path


    def set_path(self,path):
        self._path = path


    def add_noise(self,noise):
        self._noise_power += noise

    def add_latency(self,latency):
        self._latency += latency


    def next(self):
        self._path =self._path[1:]



