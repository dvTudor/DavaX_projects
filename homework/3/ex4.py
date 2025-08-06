# - Create a Python script that demonstrates the use of f-strings to format and display information in a clean and readable way.
# - Example -> define the following variables:
# name = "Alice"
# age = 30
# balance = 1234.56789
# membership_date = "2023-08-12"
# status = True
# - Use f-strings to print the following:
# 1. A sentence that introduces the user, including name and age.
# 2. The balance is formatted with:
# exactly two decimal places
# prefixed with a currency symbol ($)
# aligned to the right in a field of width 10
# 3. The membership date formatted using a placeholder like: Member since: 2023-05-15
# 4. A boolean sentence like: "Active member: Yes" if status is True, otherwise "Active member: No".

name = "Alice"
age = 30
balance = 1234.56789
membership_date = "2023-08-12"
status = True

print(f"{name} is {age}.")
print(f"Balance: {f"${balance:.2f}":>10}")
print(f"Member since: {membership_date}")
print("Active member: Yes" if status else "Active member: No")
