# - Demonstrate how to convert values between int, float, and bool. Create a script with the following variables defined:
# x = 100
# y = -30
# z = 0
# Then compare the values and “identity” of the objects.

x = 100
y = -30
z = 0

print("x:")
print(f"{x} -> {id(x)}")
x_float = float(x)
print(f"{x_float} -> {id(x_float)}")
x_bool = bool(x)
print(f"{x_bool} -> {id(x_bool)}")

print("\ny:")
print(f"{y} -> {id(y)}")
y_float = float(y)
print(f"{y_float} -> {id(y_float)}")
y_bool = bool(y)
print(f"{y_bool} -> {id(y_bool)}")

print("\nz:")
print(f"{z} -> {id(z)}")
z_float = float(z)
print(f"{z_float} -> {id(z_float)}")
z_bool = bool(z)
print(f"{z_bool} -> {id(z_bool)}")