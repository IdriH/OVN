import numpy as np
from scipy.constants import c, h, pi


class Line:



    def __init__(self,line_dict):
        self._label = line_dict['label']
        self._length = line_dict['length']
        self._state = ['free']*10
        self.successive = {}

        self._n_amplifiers = int(self.length/80e3) + 2
        # 1 amplifier every 80 km + booster + preamplifier
        self._span_length = self._length/self.n_amplifiers
        self.gain = 16 #db
        self.noise_figure = 3 #db

        #Physical parameters of the fiber
        self._alpha = 0.2e-3 #db/m
        self._beta_2 = 2.13e-26 # m Hz2-1
        self._gama = 1.27e-3
        self._Rs = 32e9 #HZ
        self._df = 50e9 #hz

    @property
    def alpha(self):
        return self._alpha

    @property
    def beta_2(self):
        return  self._beta_2

    @property
    def gama(self):
        return self._gama

    def span_length(self):
        return  self._span_length


    @property
    def n_amplifiers(self):
        return self._n_amplifiers

    @property
    def length(self):
        return self._length

    @property
    def label(self):
        return self._label
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

    def noise_generation(self, lightpath):
        # noise = 0.000000001 * signal_power * self._length  # 1e-9 * s_p * length

        return  self.ase_generation() + self.nli_generation(lightpath.signal_power, lightpath.df, lightpath.Rs)


    def propagate (self,lightpath,occupation = 'False'):
        # UPDATE LATENCY
        latency = self.latency_generation()
        lightpath.add_latency(self.latency)

        #Update noise
        signal_power = lightpath.signal_power
        noise = self.noise_generation(lightpath)
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

    def ase_generation(self):
        NF = 10 ** (self.noise_figure / 10)
        G = 10 ** (self.gain / 10)
        f = 193.414e12
        Bn = 12.5e9  # GHz
        ASE = self.n_amplifiers * h * f * Bn * NF * (G - 1)
        return ASE

    def nli_generation(self, signal_power, dfp, Rsp):

        Bn = 12.5e9  # GHz
        eta_nli = self.eta_nli(dfp, Rsp)
        nli = (signal_power ** 3) * eta_nli * self._n_amplifiers * Bn
        return nli

    def eta_nli(self, dfp, Rsp):
        df = dfp
        Rs = Rsp
        a = self.alpha / (20 * np.log10(np.e))
        Nch = 10
        b2 = self.beta_2
        e_nli = 16 / (27 * np.pi) * np.log(
            np.pi ** 2 * b2 * Rs ** 2 * Nch ** (2 * Rs / df) / (2 * a)) * self.gama ** 2 / (
                        4 * a * b2 * Rs ** 3)

        return e_nli

    def optimized_launch_power(self, eta):
        F = 10 ** (self.noise_figure / 10)
        G = 10 ** (self.gain / 10)
        f0 = 193.414e12
        opt_lp = ((F * f0 * h * G) / (2 * eta)) ** (1 / 3)
        return opt_lp

    def free_state(self):
        self._state = ['free'] * 10