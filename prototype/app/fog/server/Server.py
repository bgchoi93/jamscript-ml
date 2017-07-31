import numpy as numpy
#use to simulate inputs
#infinitely running process that sends inputs to different fog controllers 
#or creates fog controllers when new machine learning requests are needed
#responsible for requesting weights from the cloud

class Server(object):

	def __init__(self):

	def new_learning_problem(networkString):
		#load networkString from redis