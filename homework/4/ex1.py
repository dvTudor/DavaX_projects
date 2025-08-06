# - You are given a list of tuples in the following format:
#   (amount, currency, target_currency, exchange_rate)
#
# - Example:
#   data = [
#     (100, 'USD', 'EUR', 0.83),
#     (100, 'USD', 'CAD', 1.27),
#     (100, 'CAD', 'EUR', 0.65)
#   ]
# - Write code that unpacks each tuple and prints a converted amount using f-string formatting.
# - Example output: '100 USD = 83 EUR'

def convert_currency(data):
    for entry in data:
        print(f"{entry[0]} {entry[1]} = {int(entry[3]*entry[0])} {entry[2]}")

data = [
    (100, 'USD', 'EUR', 0.83),
    (100, 'USD', 'CAD', 1.27),
    (100, 'CAD', 'EUR', 0.65)
]

convert_currency(data)