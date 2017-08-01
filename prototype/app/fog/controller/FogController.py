#  handles assigning neuron computation to different devices
from prototype.app.fog.layer import Layer as layer
from prototype.app.thing.neuron import Neuron as neuron
from prototype.app.thing.neuron import FeedForwardNeuron as ffNeuron
from prototype.app.fog.network import Network as network
from prototype.app.fog.device import Device as Device
import numpy as numpy

class FogController(object):

    def __init__(self, network, devices, output_device, input_device):
        self._network = network #load from redis
        if devices is None: 
        	self._devices = []
        else:
        	self._devices = devices #for prototype simulation purposes, devices will be controller processes
        self._output_device = output_device #process/device from which output will go to
        self._output_results = [] #ordered array of results from neuron computation corresponding to ordering of the neurons
        self._layer_neurons = []

    def add_device(deviceId):
    	#add device to list
    	device = Device(deviceId,None)
    	self._devices += [device]

    def remove_device(device):
    	#remove device from devices list
    	self._devices.remove(device)
    	



    def device_on_disconnect(device):
    	#take neurons in device objects
    	#add to task queue

    	self.layer_neurons += device._neurons
    	self.remove_device(device)
    	def sort_function(device):
    		return device._neurons_count
    	self._devices = sorted(self._devices, key = sort_function)




    def task_device(device,neuron):
    	#add neuron to device _neurons
    	#send neuron task to device through device.do_computation() 
    	device.add_neuron(neuron)

    def layer_computation(layerId):
    	#read layer from redis
    	#add all neurons to task queue
    	#reinit layer_neurons
    	#add all neurons to layer_neurons
    	#neuron = task queue pop
    	#while neurons in task queue remain
    	#	for device in devices
    	#		ping device (if necessary)
    	#		__create_task(device,neuron)
       	#		remove neuron from task queue
    	#	end for
    	#	neuron = task queue pop
    	#end while

    def neuron_done(deviceId,neuronId,output):
    	#add output to output array at position [neuronId]
    	#check if layer_neurons is empty
    	#	layer_done
    	#return

    def layer_done():
    	#input = output_results
    	#send input to devices
    	#__layer_computation


    def compute_network():

if __name__=="__main__":
	#test suite 

### ------------- batch tasking vs single node tasking at a time -------------- ###
	#single node tasking is the superior solution
	#proof:
	#assumption: send time for fog to device is aprox equivalent in both cases (same amount of data)
	#case 1: computation time of node [c(n)] >= fog->device information sending f(d)
	#	since both tasking scenarios send the same of data, upload of data to device ends at approximately the same point
	#	we start computing our first node faster in single tasking however, so total time from beginning of data transfer
	#	to final response is lowered in this case 
	#	because of first node faster computation, we send responses faster, allowing for more reliability
	#case 2: c(n) < f(d)
	#	in single tasking our first node starts computing first
	#	however, since c(n) < f(d) we must wait for data transfer to complete in each case
	#	out last node is begins computation at the same time for single tasking and batch tasking
	#	no process speed up, only reliability increases