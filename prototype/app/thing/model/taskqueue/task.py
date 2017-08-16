class Task():


    def __init__(self, neuron_id, inputs):
        self.__neuron_id__ = neuron_id
        self.__inputs__ = [float(i) for i in inputs]


    def get_neuron_id(self):
        return self.__neuron_id__


    def get_inputs(self):
        return self.__inputs__