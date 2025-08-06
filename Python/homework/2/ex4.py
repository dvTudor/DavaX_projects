# - Create a script that evaluates several Boolean expressions using logical operators (and, or, not).
# The following variables are defined:
# x = 5
# y = 0
# z = -3
# 1. Check if all three numbers are greater than zero.
# 2. Check if at least one number is equal to. (zero?)
# 3. Check if none of the numbers are negative.
# Use print statements to show the results.

x = 5
y = 0
z = -3

print("All three numbers greater than zero: ")
print(x > 0 and y > 0 and z > 0)

print("At least one number equal to zero:")
print(x == 0 or y == 0 or z == 0)

print("No negative numbers: ")
print(not(x < 0 or y < 0 or z < 0))
