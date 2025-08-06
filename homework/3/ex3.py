# - Create a Python script that checks if a given word is a palindrome using slicing.
# - Hint: palindromes are 'level', 'madam'…

def check_palindrome(word):
    w1 = list(word)
    if w1 == w1[::-1]:
        print(f"{word} is palindrome")
    else:
        print(f"{word} is not palindrome")

check_palindrome("level")
check_palindrome("lever")