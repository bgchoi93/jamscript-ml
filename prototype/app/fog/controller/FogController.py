#  handles assigning neuron computation to different devices
from prototype.app.fog.layer import Layer as layer
from prototype.app.thing.neuron import Neuron as neuron
from prototype.app.thing.neuron import FeedForwardNeuron as ffNeuron
from prototype.app.fog.network import Network as network

class FogController(object):

    def __init__(self, network, devices, output_device, input_device):
        self.network = network #load from redis
        self.devices = devices #for prototype simulation purposes, devices will be controller processes
        self.output_device = output_device #process/device from which output will go to
        self.output_results = [] #ordered array of results from neuron computation corresponding to ordering of the neurons
        self.layer_neurons = Queue()

    def __add_device(device):
    	#add device to list

    def __remove_device(device):
    	#remove device from devices list

    def __device_on_disconnect(device):
    	#take neurons in device objects
    	#add to task queue

    def __task_device(device):
    	#add neuron to device _neurons
    	#send neuron task to device through device.__do_computation() 

    def __layer_computation(layerId):
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

    def __neuron_done(neuronId,output):
    	#add output to output array at position [neuronId]
    	#check if layer_neurons is empty
    	#	__layer_done
    	#return

    def __layer_done():
    	#input = output_results
    	#send input to devices
    	#__layer_computation


    def __compute_network

### ------------- batch tasking vs single node tasking at a time -------------- ###
	#single node tasking is the superior solution
	#proof:
	#assumption: send time for fog to device is aprox equivalent in both cases (same amount of data)
	#case 1: computation time of node [c(n)] => fog->device information sending f(d)
	#	since both tasking scenarios send the same of data, upload of data to device ends at approximately the same point
	#	we start computing our first node faster in single tasking however, so total time from beginning of data transfer
	#	to final response is lowered in this case 
	#	because of first node faster computation, we send responses faster, allowing for more reliability
	#case 2: c(n) < f(d)
	#	in single tasking our first node starts computing first
	#	however, since c(n) < f(d) we must wait for data transfer to complete in each case
	#	out last node is begins computation at the same time for single tasking and batch tasking
	#	no process speed up, only reliability increases