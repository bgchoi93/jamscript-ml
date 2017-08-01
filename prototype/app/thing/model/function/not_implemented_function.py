from prototype.app.thing.model.function.activation_function import ActivationFunction

class NotImplementedFunction(ActivationFunction):

    def get_function(self):
        return self.__none_function

    def __none_function(self):
        return None