import os
import subprocess as sub
import ctypes
import sys

def linux(): return sys.platform.startswith('linux')
def darwin(): return sys.platform.startswith('darwin')
def windows(): return sys.platform.startswith('win')

def get_path_to_dll():
    if linux() or darwin():
        path_to_compiled_dll = os.path.abspath('./target/release/librust.so')
    elif windows():
        path_to_compiled_dll = os.path.abspath('./target/release/rust.dll')

    if not os.path.exists(path_to_compiled_dll):
        raise EnvironmentError("In the cargo.toml of your rust folder, the [package] name MUST be 'rust' and NOTHING else. This is done so that the .dll file always has the same name.")

    return path_to_compiled_dll


def compile_rust_folder(path = 'rust', predll = False):
    path = os.path.abspath(path)
    os.chdir(path)

    result = sub.run('cargo build --release'.split(' '), stdout=sub.PIPE, stderr=sub.PIPE, text=True)

    if result.returncode == 0:
        # Success compiling!
        dll = ctypes.CDLL(get_path_to_dll())
        return dll
    else:
        print(result.stderr)
        print('Errors in rust file! Quitting...')
        quit()
