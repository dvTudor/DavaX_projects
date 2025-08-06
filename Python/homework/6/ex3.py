# - Write a function ‘check_age(age)’ that validates user input and handles different types of errors using multiple except blocks.
# - Prompt the user to enter their age (as input).
# - Attempt to convert the input to an integer:
#     1. If it fails, catch adequate ExceptionType error and print a custom error message.
#     2. If the number is negative or greater than 120, raise adequate ExceptionType error and print a custom error message.
#     3. If the input is an empty string, raise adequate ExceptionType error and print a custom error message.
#     4. In any case print 'Validation complete'.
# - Test the function by calling it with both valid and invalid inputs.

def check_age(age):
    try:
        if age == '':
            raise ValueError("No input was written")

        try:
            age = int(age)
        except ValueError as e:
            raise ValueError("Input was not integer")

        if age < 0 or age > 120:
            raise ValueError("Age cannot be negative or too high.")
    finally:
        print("Validation complete")

age = input("Write your age: ")
try:
    check_age(age)
except ValueError as e:
    print(e)