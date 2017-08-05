import numpy as numpy 

class Device:
	def __init__(self,device,neurons,__neuron_complete_callback):
		self._device = device #http remote addr
		self._neurons_count = 0
		if neurons is None:
			self._neurons = []
		else: 
			self._neurons = neurons #string list corresponding to redis nodes 			
			for neuron in self._neurons:
				self._neuron_computation(neuron)
				self._neurons_count += 1

		

	def add_neuron(neuron):
		#_neurons.add(neuron)
		#_neurons_count ++
		self._neurons += [neuron]
		self._neurons_count += 1
		self.neuron_computation(neuron)

	def neuron_computation(neuron):
		#device.do_computation(neuron) send to device
		pass



	def neuron_complete(neuronId,output,callback):
		#remove neuron from _neurons
		#	decrement
		#return neuronId,output	
		for i in range(0,len(self._neurons)):
			if neuron.id == neuronId:
				self._neurons = self._neurons[0:i] + self._neurons[i+1:]
				self._neurons_count -= 1
				callback(neuronId,output)


