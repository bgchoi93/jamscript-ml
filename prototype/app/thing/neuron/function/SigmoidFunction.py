from ActivationFunction import ActivationFunction
import math


class SigmoidFunction(ActivationFunction):

    def get_function(self):
        return self.__sigmoid

    def __sigmoid(self, weights, bias):
        return 1 / (1 + math.exp(-math.fsum(weights) - bias))
