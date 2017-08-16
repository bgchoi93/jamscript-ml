#handle receiving requests here

import numpy as numpy
from flask import Flask, request, Response, abort
from prototype.app.fog.controller import FogController as fog
from prototype.app.fog.server.Server import Server as Server

#service to receive http request
#
#


server = Server()

app = Flask(__name__)

@app.route('/')
def hello_world():
	print (request.remote_addr)
	return 'Hello World!'


#create new fog controller for a new problem domain
#
#
@app.route('/<problemName>', methods = ['POST','GET'])
def ml_problem(problemName):
    if request.method == 'POST':
    	server.add_device(request.remote_addr)
    	server.new_learning_problem(problemName,request.remote_addr)
    	return 'request.remote_addr %s' % request.remote_addr
    elif request.method == 'GET':
    	return 'request.remote_addr %s' % request.remote_addr



#a neuron of the problemName domain has completed, run appropriate operations
#
#
@app.route('/<problemName>/neuron_complete', methods = ['POST'])
def neuron_complete(problemName):
	if request.method == 'POST':
		params = request.get_json()
		server._controllers[problemName].neuron_done(request.remote_addr,request.form[neuronId],request.form[output])



#add a device to the network
#
#
@app.route('/subscribe',methods = ['POST'])
def add_device():
	server.add_device(request.remote_addr)
