# - Create a text file named 'students.txt' containing student names, one per line.
# - Use a context manager to open and read the file.
# - Create a new file 'filtered.txt' and write only the names that start with a vowel (A, E, I, O, U).

import os

with open("students.txt") as f:
    data = f.read()

names = data.split('\n')
vowels = ['A', 'E', 'I', 'O', 'U']

with open("filtered.txt", 'w+') as f:
    filtered_names = [name for name in names if name[0][0] in vowels]
    for i, name in enumerate(filtered_names):
        f.write(name)
        if i != len(filtered_names) - 1:
            f.write('\n')
