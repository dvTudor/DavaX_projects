# - Create a class ‘BankAccount’ with a private balance attribute.
# - Use ‘@property’ and ‘@setter’ to allow reading and updating the balance, but prevent the balance from being set to a negative value.
# - Add a method ‘deposit(amount)’ and ‘withdraw(amount)’ that update balance safely.
# - Raise exceptions if invalid operations are attempted.
# - Create an object, test deposits, withdrawals, and invalid inputs.

class BankAccount:

    def __init__(self, balance=0):
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, new_value):
        if new_value >= 0:
            self.__balance = new_value
        else:
            raise ValueError("Cannot set a negative balance")

    def deposit(self, amount):
        if amount >= 0:
            self.__balance += amount
        else:
            raise ValueError("Cannot deposit a negative amount")

    def withdraw(self, amount):
        if self.__balance - amount < 0:
            raise ValueError("Cannot withdraw more than the balance")
        if amount >= 0:
            self.__balance -= amount
        else:
            raise ValueError("Cannot withdraw a negative amount")

acc = BankAccount()
print(f"Balance of newly created account: {acc.balance}")
acc.balance = 50
print(f"Updated balance: {acc.balance}")

# trying to set a negative balance
try:
    acc.balance = -50
except ValueError as e:
    print(e)

# trying to deposit a negative amount
try:
    acc.deposit(-5)
except ValueError as e:
    print(e)

try:
    acc.deposit(5)
except ValueError as e:
    print(e)
print(f"Updated balance after correct deposit: {acc.balance}")

# trying to withdraw a negative amount
try:
    acc.withdraw(-5)
except ValueError as e:
    print(e)

try:
    acc.withdraw(5)
except ValueError as e:
    print(e)
print(f"Updated balance after correct withdrawal: {acc.balance}")

# trying to withdraw too much
try:
    acc.withdraw(60)
except ValueError as e:
    print(e)