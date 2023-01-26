
class Connection:

    def __init__(self,input,output,signal_power):
        self._input_node = input
        self._output_node = output
        self._signal_power = signal_power
        self._latency = 0
        self._snr = 0
        self._rb = 0


    @property
    def bit_rate(self):
        return self._rb
    @bit_rate.setter
    def bit_rate(self,value):
        self._rb = value


    @property
    def input(self):
        return self._input_node
    @property
    def output(self):
        return self._output_node

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self,latency):
        self._latency = latency
    @property
    def snr(self):
        return self._snr
    @snr.setter
    def snr(self,snr):
        self._snr = snr
