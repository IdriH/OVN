


c = 299792458
class Line:



    def __init__(self,line_dict):
        self.label = line_dict['label']
        self.length = line_dict['length']
        self._state = ['free']*10
        self.successive = {}


    @property
    def get_label(self):
        return self.label
    @property
    def get_successive(self):
        return self.successive

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self,state):
        state = [s.lower().strip() for s in state]
        if set(state).issubset(set(['free','occupied'])):
            self._state = state
        else:
            print('Error:Line state not recognized,Value:',
                  set(state)-set(['free','occupied']))


    def latency_generation(self):
        self.latency = self.length / (2/3 * c)

    def noise_generation(self,signal_power):
        self.noise_power = 1e-9 * signal_power * self.length
        return self.noise_power


    def propagate (self,lightpath,occupation = 'False'):
        # UPDATE LATENCY
        latency = self.latency_generation()
        lightpath.add_latency(self.latency)

        #Update noise
        signal_power = lightpath.signal_power
        noise = self.noise_generation(signal_power)
        lightpath.add_noise(noise)


        #Update line state
        if occupation:
            channel = lightpath.channel
            new_state = self.state[:]
            new_state[channel] = 'occupied'
            self.state = new_state

        node = self.successive[lightpath._path[0]]
        lightpath = node.propagate(lightpath,occupation)

        return lightpath
