import os
import subprocess as sub
import ctypes
import sys

def linux(): return sys.platform.startswith('linux')
def darwin(): return sys.platform.startswith('darwin')
def windows(): return sys.platform.startswith('win')

def get_path_to_dll(predll = False):
    if linux() or darwin():
        path_to_compiled_dll = os.path.abspath('./target/release/librust.so')
    elif windows():
        path_to_compiled_dll = os.path.abspath('./target/release/rust.dll')

    if not os.path.exists(path_to_compiled_dll):
        if predll == False:
            raise EnvironmentError("In the cargo.toml of your rust folder, the [package] name MUST be 'rust' and NOTHING else. This is done so that the .dll file always has the same name.")
        elif predll == True:
            raise EnvironmentError("You enabled predll, But no compiled dll was found.")

    return path_to_compiled_dll
def help_user_with_common_errors(result):
    if result.returncode == 101:
        print('Seems like in your rust/src folder, There is no lib.rs file. Instead of a main.rs file, Make a lib.rs file in that directory.')


def compile_rust_folder(path = 'rust', predll = False):
    path = os.path.abspath(path)
    os.chdir(path)

    if not predll:
        result = sub.run('cargo build --release'.split(' '), stdout=sub.PIPE, stderr=sub.PIPE, text=True)

        if result.returncode == 0:
            # Success compiling!
            dll = ctypes.CDLL(get_path_to_dll())
            return dll
        else:
            help_user_with_common_errors(result)
            print(result.stderr)
            print('Errors in rust file! Quitting...', result.returncode)
            quit()
    elif predll:
        # User is telling that the dll is already compiled and for speed we do not need to compile it again.
        dll = ctypes.CDLL(get_path_to_dll(True))
        return dll
