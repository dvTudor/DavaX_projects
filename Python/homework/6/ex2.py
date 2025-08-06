# - You are given two lists:
#     names = ["Lucas", "Nataly", "Megi", "Maria", "Steven"]
#     scores = [85, 92, 78, 81, 67]
# - Combine the names and scores into a single collection of (name, score) pairs.
# - Sort the result in descending order by score using a ‘lambda’ function.
# - Only include students who scored 80 or above in the final output.
# - Print the sorted list of (name, score) pairs.
#
#
# - Expected output:
#     Nataly: 92
#     Lucas: 85
#     Maria: 81

names = ["Lucas", "Nataly", "Megi", "Maria", "Steven"]
scores = [85, 92, 78, 81, 67]

grades = {name:score for name, score in zip(names, scores)}
print(grades)
sorted_grades = {name:score for name, score in sorted(grades.items(), key=lambda item: -item[1])}
print(sorted_grades)
passing_grades = {name:score for name, score in sorted_grades.items() if score>=80}
print(passing_grades)