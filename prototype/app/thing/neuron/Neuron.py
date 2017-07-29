class Neuron(object):
    def __init__(self, id, activation_function, inputWeights, bias):
        self.id = id
        self._activation_function = activation_function
        self._weights = inputWeights
        self._bias = bias

    def calculate(self):
        pass

    def get_activation_function(self):
        return self._activation_function

    def get_weights(self):
        return self._weights

    def get_bias(self):
        return self._bias
