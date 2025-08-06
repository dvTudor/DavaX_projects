# - Write a Python script that changes the target word into a new word from a sentence without using the replace() function.
#
# - Example:
# sentence = "Python is fun because Python is powerful"
# target_word = "Python"
# new_word = "Programming"

def replace_word(sentence, target_word, new_word):
    if sentence.find(target_word) == -1:
        return sentence
    else:
        new_sentence = sentence
        while new_sentence.find(target_word) != -1:
            s = list(new_sentence)
            # print(s)
            w = list(new_word)
            # print(w)
            w.reverse()
            pos = new_sentence.find(target_word)
            for _ in range(len(target_word)):
                s.pop(pos)
            # print(s)
            for _ in range(len(new_word)):
                s.insert(pos, w[0])
                w.pop(0)
            new_sentence = ''.join(s)
        return new_sentence

sentence = "Python is fun because Python is powerful"
target_word = "Python"
new_word = "Programming"

print(sentence)
print(replace_word(sentence, target_word, new_word))
