# - Create a program that asks the user to enter a year and then checks whether that year is a leap year.
# Print “This is a leap year.” or “This isn’t a leap year.” based on the provided year.
# Hint:
# - use “input()” function -> year = input(“Enter desired year: ”)
# - the input() function returns a “str” type

year = input("Enter desired year: ")
year = int(year)
leap = 0

if year % 4 == 0 or year % 400 == 0:
    leap = 1

if year % 4 == 0 and year % 100 == 0 and year % 400 != 0:
    leap = 0

if leap == 1:
    print("This is a leap year.")
else:
    print("This isn't a leap year.")