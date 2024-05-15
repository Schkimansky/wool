from typing import Any
from rust_compiler import compile_rust_folder

def load_function(dll, name, arguments=None, return_type=None):
    func = getattr(dll, name)
    if arguments: func.argtypes = arguments
    if return_type: func.restype = return_type

    return func

# When you make a class in the rust file, you need to make methods that create the class and then return its pointer. This loads a function thats designed to return the pointer to a class
def load_create_function(function):
    pass
