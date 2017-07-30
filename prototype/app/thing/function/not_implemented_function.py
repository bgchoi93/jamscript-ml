from prototype.app.thing.function.activation_function import ActivationFunction

class NotImplementedFunction(ActivationFunction):

    def get_function(self):
        return self.__none_function

    def __none_function(self):
        return None