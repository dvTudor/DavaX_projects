# - You are given the following list of numbers:
# numbers = [10, 20, 30, 40, 50]
#
# - Access and print:
# the first element
# the last element
# the middle element (use len() to calculate the index)
# - Add the number 60 to the end of the list.
# - Insert the number 15 at index 1.
# - Remove the last element from the list.
# - Print the length of the list.
# - Sort the list and print it.

numbers = [10, 20, 30, 40, 50]
print(numbers[0])
print(numbers[-1])
print(numbers[round(len(numbers)/2)])

numbers.append(60)
numbers.insert(1, 15)
numbers.pop(-1)
print(len(numbers))
numbers.sort()
print(numbers)
