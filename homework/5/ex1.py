# - Write a Python script that checks whether two words are anagrams of each other.
# - Use a dictionary to count the frequency of each letter in both words.
# - Define two words, e.g. "listen" and "silent"
# - Modify one of the dictionaries (e.g., delete one letter) and print both to show the effect.

def check_anagram(word_1, word_2):
    w1 = list(word_1)
    w2 = list(word_2)
    letter_counts_1 = []
    letter_counts_2 = []

    for i in range(len(w1)):
        if w1[i] != "":
            count = 1
            for j in range(i+1, len(w1)):
                if w1[i] == w1[j]:
                    count += 1
                    w1[j] = ""
            letter_counts_1.append(count)

    w1_copy = [c for c in w1 if c != ""]
    dict_1 = {}
    i = 0
    for c in w1_copy:
        dict_1[c] = letter_counts_1[i]
        i += 1

    for i in range(len(w2)):
        if w2[i] != "":
            count = 1
            for j in range(i+1, len(w2)):
                if w2[i] == w2[j]:
                    count += 1
                    w2[j] = ""
            letter_counts_2.append(count)

    print(dict_1)

    w2_copy = [c for c in w2 if c != ""]
    dict_2 = {}
    i = 0
    for c in w2_copy:
        dict_2[c] = letter_counts_2[i]
        i += 1

    # dict_2.popitem()

    print(dict_2)

    return dict_1 == dict_2

print(check_anagram("secure", "rescue"))
