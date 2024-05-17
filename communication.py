from typing import Any
import ctypes as c

C_TYPES = {'int': c.c_int, 'str': c.c_char_p, int: c.c_int, str: c.c_char_p}

class DataType: pass

def load_function(function, arguments=None, return_type=None):
    func = function
    if arguments: func.argtypes = arguments
    if return_type: func.restype = return_type

    def funtion_caller(*args, **kwargs):
        parameter_values = [*args] + [val for key, val in kwargs.items()]
        
        processed_values = []
        for paramval in parameter_values:
            if type(paramval) == str:
                processed_values.append(paramval.encode())
            else:
                processed_values.append(paramval)

        return func(*processed_values)

    return funtion_caller

def make_rust_class(class_name: str, parameters: dict[str, DataType]):

    class RustClass(c.Structure):
        _fields_ = [(key, C_TYPES[val]) for key, val in parameters.items()]

        def __init__(self, *args, **kwargs):

            if len(args)-1 + len(kwargs.keys())-1 != len(parameters.keys()) - 2:
                raise ValueError('Invalid parameters')

            for i, key in enumerate(parameters.keys()):
                try:
                    setattr(self, key, args[i])
                except IndexError:
                    setattr(self, key, kwargs[key])
        
        def __getattribute__(self, name: str) -> Any:
            try:
                return super().__getattribute__(name)
            except AttributeError:
                try:
                    rust_func = getattr(dll, f"{class_name}_{name}")
                except AttributeError:
                    raise AttributeError(name, 'is a property that does not exist.')

                def python_func_layer(*args, **kwargs):
                    return rust_func(c.byref(self), *args, **kwargs)
                return python_func_layer # return a callable function. This function is basically the rust function of the rust class, but automatically gives self AND, can be accessed easily by doing: my_rust_class.rust_method()

    return RustClass
