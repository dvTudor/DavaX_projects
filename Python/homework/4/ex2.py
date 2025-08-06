# - Write a Python script that prints the sum of all odd numbers from 1 to 100.

s = 0

for i in range(100):
    if i % 2 == 1:
        s = s + i

print(s)