# - Use list comprehension to create a list of squares from 1 to 10.
# - Use set comprehension to create a set of numbers dividable by 7 between 1 and 50.
# - Use dictionary comprehension to create a new dictionary of only students who passed
# (>= 60).
# score = {"Alice": 85, "Bob": 59, "Charlie": 92}
# - Use nested dictionary comprehension to create a weekly attendance log where:
# - Students attend only on Monday and Wednesday
# - All other days are marked as False
# - Input:
#     students = ["Michael", "David", "Liza"]
#     weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri"]
# - Expected output:
# {
#     " Liza ": {"Mon": True, "Tue": False, "Wed": True, "Thu": False, "Fri": False},
#     " David ": {"Mon": True, "Tue": False, "Wed": True, "Thu": False, "Fri": False},
#     " Michael ": {"Mon": True, "Tue": False, "Wed": True, "Thu": False, "Fri": False}
# }

squares = [(i+1)**2 for i in range(10)]
print(squares)

divisible_by_7 = {(i+1) for i in range(50) if (i+1)%7 == 0}
divisible_by_7 = sorted(divisible_by_7)
print(divisible_by_7)

score = {"Alice": 85, "Bob": 59, "Charlie": 92}
passed = {key:score[key] for key in score if score[key]>=60}
print(passed)

students = ["Michael", "David", "Liza"]
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri"]

def check_attendance(day):
    if day == "Mon" or day == "Wed":
        return True
    else:
        return False

attendance = {student: {weekday: check_attendance(weekday) for weekday in weekdays} for student in students}
print(attendance)