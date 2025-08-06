# - Define two classes: ‘EmailNotification’ and ‘SMSNotification’.
# - Both should implement a method ‘send(message)’ that prints a different format of notification.
# - Write a function ‘send_bulk(notifiers, message)’ that loops through any list of objects
#   and calls ‘.send()’ on them without checking their type.
# - Demonstrate that this works using duck typing.

from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailNotification(Notification):
    def send(self, message):
        print(f"Email from john.doe@gmail.com: {message}")

class SMSNotification(Notification):
    def send(self, message):
        print(f"SMS from contact John Doe: {message}")

def send_bulk(notifiers, message):
    for notifier in notifiers:
        notifier.send(message)

notifiers = [EmailNotification(), SMSNotification(), EmailNotification()]
message = "Hello there"
send_bulk(notifiers, message)