# - Write a program that asks the user to guess a secret number (hardcode it to e.g. 7).
# - Stop the loop immediately once the correct number is guessed and print the message.
# - If the user doesn't guess the number within the allowed number of attempts (e.g. 3), display a message at the end.

secret_number = 7

guessed = 0
tries = 3

while guessed == 0 and tries > 0:

    guess = input("Guess: ")

    if int(guess) == secret_number:
        guessed = 1
        print("Congratulations!")
    else:
        tries -= 1
    
    if tries == 0:
        print("Better luck next time")
