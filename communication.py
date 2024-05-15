from typing import Any
from rust_compiler import compile_rust_folder

def load_function(dll, name, arguments=None, return_type=None):
    func = getattr(dll, name)
    if arguments: func.argtypes = arguments
    if return_type: func.restype = return_type

    return func

if __name__ == '__main__':
    # Testing library
    dll = compile_rust_folder()
    counter = dll.Counter_new(50)
    dll.Counter_count(counter)
    print(dll.Counter_get(counter))
