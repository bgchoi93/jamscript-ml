import prototype.app.thing.function.ActivationFunctionFactory as aff
from prototype.app.thing.neuron import Neuron


class FeedForwardNeuron(Neuron):

    def __init__(self, id, inputs, weights, bias):
        super(FeedForwardNeuron, self).__init__(id, aff.get_activation_function("sigmoid"), inputs, weights, bias)

    def calculate(self):
        return self._activation_function.get_function()(self._inputs, self._weights, self._bias)
