from prototype.app.thing.function.sigmoid_function import SigmoidFunction
from prototype.app.thing.function.not_implemented_function import NotImplementedFunction

activation_functions = {
    'sigmoid' : SigmoidFunction()
}

def get_activation_function(function_name):
    return activation_functions.get(function_name, NotImplementedFunction)
