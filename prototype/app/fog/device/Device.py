#handle sending requests here

import json
import numpy as numpy 
import requests

headers = {'Content-type':'application/json','Accept':'application/json'}

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

		

	def add_neuron(neuron,inputs):
		self._neurons += [neuron]
		self._neurons_count += 1
		self.neuron_computation(neuron,inputs)

	def neuron_computation(neuron,inputs):
		payload = {'neuron_id':neuron}
		if inputs != None: 
			payload['inputs'] = inputs
		task = requests.post("http://localhost:5000/task", headers=headers, data=payload)
		return task.json()



	def neuron_complete(neuronId):
		for i in range(0,len(self._neurons)):
			if neuron.id == neuronId:
				self._neurons = self._neurons[0:i] + self._neurons[i+1:]
				self._neurons_count -= 1


