# - Define a function calculate() that can take any number of numeric arguments and apply a basic arithmetic operation (+, -, *, /)
# to them.
# - Set the default operation to addition (+).
# - Handle edge cases:
#     1. If no numbers are passed, return 0
#     2. Handle the division by 0
# - Return the result of applying the operation to all numbers.
# - Call the function multiple times using:
#     1. Positional arguments
#     2. Named operation argument
# Example usage:
#     calculate(2, 3, 4, operation='*')
#     calculate(10, 0, operation='/')
#     calculate(operation='-')

import numpy as np

def calculate(*args, operation='+'):
    if len(args) == 0:
        return 0
    if args[-1] == 0:
        return "Cannot divide by 0"
    if operation == '+':
        return np.sum(args)
    if operation == '-':
        return args[0] - np.sum(args[1:])
    if operation == '*':
        return np.prod(args)
    if operation == '/':
        return args[0] / int(np.prod(args[1:]))
    else:
        return "Try again with the appropriate arguments"

print(calculate(2, 3, 4, operation='*'))
print(calculate(10, 0, operation='/'))
print(calculate(operation='-'))
print(calculate(3, 4))
print(calculate(3, 4, operation='-'))
print(calculate(6, 2, operation='/'))
print(calculate(16, 2, 2, operation='/'))
print(calculate(16, 2, 2, operation='-'))