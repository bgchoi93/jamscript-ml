from SigmoidFunction import SigmoidFunction
from NotImplementedFunction import NotImplementedFunction

activation_functions = {
    'sigmoid' : SigmoidFunction()
}

def get_activation_function(function_name):
    return activation_functions.get(function_name, NotImplementedFunction)
