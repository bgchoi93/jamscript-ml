# handles assigning neuron computation to different devices
# create one of these objects every time you receive a problem 
from prototype.app.fog.device import Device as Device
import numpy as numpy
class FogController:
    def __init__(self, network, devices, output_device, inputs):
        self._network = network #network string name
        self._devices = []
        for device in devices:
            add_device(device)
        self._output_device = Device(output_device) #process/device from which output will go to
        self._output_results = inputs #ordered array of results from neuron computation corresponding to ordering of the neurons
        self._layer_neurons = [] #array of neurons
        self._compute = compute_network(0)
        self._db = redis.StrictRedis('localhost', 6379, 0, charset="utf-8", decode_responses=True)
        

    def ping_devices(self):
        pass
        #for device in self._devices:
            #ping device
            #remove if no response
        #sort

    def add_device(self,deviceId):
    	#add device to list
        device = Device(deviceId,None)
        self._devices += [device]

    def remove_device(self,deviceId):
        for device in self._devices:
            if (device._device == deviceId):
                self._devices.remove(device)
        def sort_function(device):
            return device._neurons_count
        self._devices = sorted(self._devices, key = sort_function)
    
    def get_layer_and_populate(layerId):
        pass
    
    def layer_computation(self,layerId):
        self.ping_devices()
        inputs = self._output_results
        self._output_results = []
        task_Queue = Queue()
        if self._db.sismember("networks",self._network):
            layer = self._db.zrange(self._network,layerId,layerId)
            if layer:
                neurons_list_name = rdb.hget(layer[0],"neurons")
                self._layer_neurons = rdb.zrange(neurons_list_name,0,rdb.zcard(neurons_list_name))
            else:
                print "no layers"
                return False
        else:
            print "no network"
            return False
        for neuron in self._layer_neurons:
            task_Queue.put(neuron)
        neuron= task_Queue.get()
        while not task_Queue.empty():
            for device in self._devices:
                device.add_neuron(neuron)
            neuron=task_Queue.get()
        return True
    
    def neuron_done(self,deviceId,neuronId,output):
        self._output_results[neuronId] = output
        for device in self._devices:
            if device._device == deviceId:
                device.neuron_complete(neuronId)
        if (len(self._layer_neurons) == 0):
            self._compute()
        return self._output_results
    
    def compute_network(self,inputs):
        layer_num = inputs
        def increment_layer():
            nonlocal layer_num
            layer_num += 1
            self.layer_computation(layer_num)
            print(layer_num)
        return increment_layer
    
    def send_results():
        pass

if __name__=="__main__":
    fogger = FogController()
    fogger.compute_network(0)
    closure = fogger.compute_network()
    closure()
    closure()
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