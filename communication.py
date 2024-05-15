from typing import Any
from rust_compiler import compile_rust_folder
import ctypes as c

C_TYPES = {'int': c.c_int, 'str': c.c_char_p, int: c.c_int, str: c.c_char_p}

class DataType: pass

def load_function(dll, name, arguments=None, return_type=None):
    func = getattr(dll, name)
    if arguments: func.argtypes = arguments
    if return_type: func.restype = return_type

    return func

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

# Tutorial!
if __name__ == '__main__':
    dll = compile_rust_folder()

    Calculator = make_rust_class('Calculator', {'x': int, 'y': int})

    # I dont know whether or not passing strings works currently.
    calculator = Calculator(2,3)

    print("Result:", calculator.add(20))