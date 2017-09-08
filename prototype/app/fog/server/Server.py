import numpy as numpy
import redis
from flask import Flask, request
from prototype.app.fog.controller import FogController as fog
#controls fog controllers so you can have multiple domains
#controls devices

class Server(object):
    def __init__(self):
        self._devices = []
        self._controllers = {}
        self._db = redis.StrictRedis(host='localhost',port=6379,db=0)

    def new_learning_problem(networkString,outputDevice,inputs):
        new_fog = fog(networkString,self._devices,outputDevice,inputs)
        self._controllers[networkString] = new_fog
        return new_fog

    def add_device(self,deviceId):
        for i in range(0, len(self._devices)):
            if (self._devices[i] == request.remote_addr):
                return self._devices
            elif(i == len(server._devices)):
                self._devices += [deviceId]
                for controller in self._controllers:
                    controller.add_device(deviceId)
        return self._devices

    def remove_device(deviceId):
        self._devices.remove(deviceId)
        for controller in self._controllers:
            controller.remove_device(deviceId)
        return self._devices

    def get_devices():
        return self._devices