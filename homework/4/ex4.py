# - You are given a list of fruits:
# fruits = ['apple', 'banana', 'cherry', 'date']
# - Print each fruit with:
# 1. Its index - starting from index 1
# 2. Its name
# 3. and the number of letters in the fruit name
# - Format the output like this:
# 1: apple (5 letters)
# 2: banana (6 letters)
# 3: cherry (6 letters)
# 4: date (4 letters)

fruits = ['apple', 'banana', 'cherry', 'date']

for i in range(len(fruits)):
    print(f"{i+1}: {fruits[i]} ({len(fruits[i])} letters)")