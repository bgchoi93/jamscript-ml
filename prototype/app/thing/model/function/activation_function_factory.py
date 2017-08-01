from prototype.app.thing.model.function.not_implemented_function import NotImplementedFunction
from prototype.app.thing.model.function.sigmoid_function import SigmoidFunction


activation_functions = {
    'sigmoid': SigmoidFunction()
}


def get_activation_function(function_name):
    return activation_functions.get(function_name, NotImplementedFunction)
