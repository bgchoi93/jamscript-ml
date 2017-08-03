import numpy as numpy
from flask import Flask, request,
from prototype.app.fog.controller import FogController as fog

server = Server()

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/<problemName>', methods = ['POST','PUT'])
def ml_problem(problemName):
    # show the user profile for that user
    if request.method == 'POST':
    	newProblem = fog(problemName,server.get_devices(),request.remote_addr)
    	return 'problemName %s' % problemName
    else