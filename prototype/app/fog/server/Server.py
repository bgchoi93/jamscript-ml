import numpy as numpy
from flask import Flask, request,
from prototype.app.fog.controller import FogController as fog
#use to simulate inputs
#infinitely running process that sends inputs to different fog controllers 
#or creates fog controllers when new machine learning requests are needed
#responsible for requesting weights from the cloud


class Server(object):

	def __init__(self):
		self._devices = []

	def new_learning_problem(networkString):
		#load networkString from redis
		#
		pass

	def add_device(deviceId):
    	#add device to list
    	device = Device(deviceId,None)
    	self._devices += [device]
    	return

    def remove_device(device):
    	#remove device from devices list
    	self._devices.remove(device)
    	return
    
    def get_devices():
    	return self._devices	

    def device_on_disconnect(device):
    	#take neurons in device objects
    	#add to task queue

    	self.layer_neurons += device._neurons
    	self.remove_device(device)
    	def sort_function(device):
    		return device._neurons_count
    	self._devices = sorted(self._devices, key = sort_function)