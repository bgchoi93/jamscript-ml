#  handles assigning neuron computation to different devices


class FogController(object):

    def __init__(self, network, devices, output_device, input_device):
        self.network = network
        self.devices = devices
        self.output_device = output_device
        self.input_device = input_device
