


c = 299792458
class Line:



    def __init__(self,line_dict):
        self.label = line_dict['label']
        self.length = line_dict['length']
        self.successive = {}


    @property
    def get_label(self):
        return self.label
    @property
    def get_successive(self):
        return self.successive


    def latency_generation(self):
        self.latency = self.length / (2/3 * c)

    def noise_generation(self,signal_power):
        self.noise_power = 1e-9 * signal_power * self.length
        return self.noise_power

    def propagate (self,signal_information):
# UPDATE LATENCY
        latency = self.latency_generation()
        signal_information.add_latency(self.latency)
#Update noise
        signal_power = signal_information.get_signal_power
        noise = self.noise_generation(signal_power)
        signal_information.add_noise(noise)
        node = self.successive[signal_information._path[0]]
        signal_information = node.propagate(signal_information)
        return signal_information
