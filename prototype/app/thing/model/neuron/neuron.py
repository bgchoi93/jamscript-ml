class Neuron(object):

    def __init__(self, neuron_id, activation_function, inputs, weights, bias):
        self._neuron_id = neuron_id
        self._activation_function = activation_function
        self._inputs = inputs
        self._weights = weights
        self._bias = bias

    def calculate(self):
        pass


    def get_neuron_id(self):
        return self._neuron_id


    def get_activation_function(self):
        return self._activation_function

    def get_inputs(self):
        return self._inputs

    def get_weights(self):
        return self._weights

    def get_bias(self):
        return self._bias
