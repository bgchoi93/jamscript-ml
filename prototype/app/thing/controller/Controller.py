#handles assigning neuron computation to different devices
from prototype.app.thing.Layer import Layer as Layer  
from prototype.app.thing.Network import Network as Network

class FogController(object)
	def __init__(self,network,devices,outputDevice,inputDevice)
		self.network = network
		self.devices = devices
		self.outputDevice = outputDevice
		self.inputDevice = inputDevice
