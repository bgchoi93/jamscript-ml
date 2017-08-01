from prototype.app.thing.model.neuron.neuron import Neuron

import prototype.app.thing.model.function.activation_function_factory as aff


class FeedForwardNeuron(Neuron):

    def __init__(self, neuron_id, inputs, weights, bias):
        super().__init__(neuron_id, aff.get_activation_function("sigmoid"), inputs, weights, bias)

    def calculate(self):
        return self._activation_function.get_function()(self._inputs, self._weights, self._bias)
