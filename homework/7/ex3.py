# - Create a Python module named ‘report.py’ containing a function ‘generate_report(data: dict)’.
# - The function should accept a dictionary of student names and scores, and return a formatted string report.
# - In a separate file, import the function and call it with data such as:
#   ‘{'Lisa': 85, 'Bart': 72, 'Homer': 91}’
# - Only include students who scored 80 or above in the final report.
# - Use string formatting and sorting to structure the output.

from report import generate_report

grades = {'Lisa': 85, 'Bart': 72, 'Homer': 91}

for grade in generate_report(grades):
    print(grade)
