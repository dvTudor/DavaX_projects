# Given a dictionary where multiple keys may have the same value, invert it - such that values become keys,
# and keys become elements of a list.
# Example:
#     grades = {
#         "Alice": "A",
#         "Bob": "B",
#         "Charlie": "A",
#         "Diana": "C"
#     }
# Expected output:
#     {
#         "A": ["Alice", "Charlie"],
#         "B": ["Bob"],
#         "C": ["Diana"]
#     }

def invert_dictionary(dictionary):

    values = []
    for x in dictionary:
        values.append(dictionary[x])
    values_set = sorted(set(values))

    new_dictionary = {}
    for value in values_set:
        keys = []
        for key in dictionary:
            if dictionary[key] == value:
                keys.append(key)
        new_dictionary[value] = keys

    return new_dictionary

grades = {
        "Alice": "A",
        "Bob": "B",
        "Charlie": "A",
        "Diana": "C"
    }

print(invert_dictionary(grades))