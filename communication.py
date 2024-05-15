# from typing import Any
# from rust_compiler import compile_rust_folder

# def load_function(dll, name, arguments=None, return_type=None):
#     func = getattr(dll, name)
#     if arguments: func.argtypes = arguments
#     if return_type: func.restype = return_type

#     return func

# if __name__ == '__main__':
#     # Testing library
#     dll = compile_rust_folder()
#     counter = dll.Counter_new(50)
#     dll.Counter_count(counter)
#     print(dll.Counter_get(counter))

import numpy as np
import matplotlib.pyplot as plt

# Define the range of values for o
o_values = np.linspace(0, 10, 400)  # Adjust the range as needed

# Define the constant parameter a
a = 5  # Adjust the value of 'a' as needed

# Calculate r for each value of o
r_values = np.sin((a / 5) * o_values)

# Plot the curve
plt.plot(o_values, r_values, label=r'$r = \sin\left(\frac{a}{5} \cdot o\right)$')
plt.xlabel('o')
plt.ylabel('r')
plt.title('Visualization of r = sin(a/5 o)')
plt.legend()
plt.grid(True)
plt.show()
