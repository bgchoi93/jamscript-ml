#handles assigning neuron computation to different devices

class FogController(object):
	def __init__(self,network,devices,outputDevice,inputDevice):
		self.network = network
		self.devices = devices
		self.outputDevice = outputDevice
		self.inputDevice = inputDevice
