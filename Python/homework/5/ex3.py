# - There is a tech conference, and attendees are listed for three sessions:
# testing, development and devops.
# - Each attendee can choose one or more sessions.
# testing = {“Ana, "Bob", "Charlie", "Diana"}
# development = {"Charlie", "Eve", "Frank", "Ana"}
# devops = {"George", "Ana", "Bob", "Eve"}
# - Find attendees who attended all three sessions.
# - Find attendees who attended only one session.
# - Check if all testing attendees are also in the devops session.
# - Get a set of all unique attendees and sort them alphabetically.
# - Create a copy of the development set and clear the original.

testing = {"Ana", "Bob", "Charlie", "Diana"}
development = {"Charlie", "Eve", "Frank", "Ana"}
devops = {"George", "Ana", "Bob", "Eve"}

all_sessions = testing.intersection(development, devops)
print(f"Attendees for all sessions: {all_sessions}")

only_one_session_1 = testing.difference(development, devops)
only_one_session_2 = development.difference(testing, devops)
only_one_session_3 = devops.difference(testing, development)
print(f"Attendees for only one sessions: {only_one_session_1 | only_one_session_2 | only_one_session_3}")

if testing.difference(devops):
    print("Not all testing attendees are in the devops session.")
else:
    print("All testing attendees are in the devops session.")

all_attendees = testing | development | devops
all_attendees = sorted(all_attendees)
print(f"All attendees: {all_attendees}")

development_copy = development.copy()
development.clear()
print(f"Development: {development}")
print(f"Development copy: {development_copy}")
