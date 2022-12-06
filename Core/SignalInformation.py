from typing import Any


class SignalInformation:


    def __init__(self,signal_power,noise_power,latency,path):
        self.__signal_power = signal_power
        self.__noisepower = 0.0
        self.__latency = 0.0
        self.__path = path



    @property
    def get_signal_power(self):
        return self.__signal_power

    @signal_power.setter
    def set_signal_power(self,signal_power):
        self.__signal_power = signal_power

    @property
    def get_noise_power(self):
        return self.__noisepower

    @noise_power.setter
    def set_noise_power(self,noise_power):
        self.__noisepower = noise_power

    @property
    def __get_latency(self):
        return self.__latency

    @set_latency
    def set__latency(self,latency):
        self.__latency = latency

    @property
    def get_path(self):
        return self.__path

    @set_path
    def set_path(self,path):
        self.__path = path


    def update_path(self,crossed_node):
        self.__path.add(crossed_node)


