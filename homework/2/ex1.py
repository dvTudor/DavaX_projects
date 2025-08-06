# - Write a simple script to demonstrate that integers and floats are immutable.

# integer
a = 3
print(f"{a} -> {id(a)}")
a = 4
print(f"{a} -> {id(a)}")

# float
b = 3.5
print(f"{b} -> {id(b)}")
b = 4.5
print(f"{b} -> {id(b)}")

# meanwhile lists which are mutable
L = [1, 2, 3]
print(f"{L} -> {id(L)}")
L[0] = 0
print(f"{L} -> {id(L)}")