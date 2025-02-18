import time

class EventCondition:
    def __init__(self, timeout, callback):
        self.timeout = timeout
        self.callback = callback
        self.last_time = 0

class EventTimer:
    def __init__(self):
        self.events = []

    def add(self, timeout, callback):
        self.events.append(EventCondition(timeout, callback))

    def handle(self, current_time, args=None):
        for event in self.events:
            if (current_time - event.last_time) >= event.timeout:
                event.last_time = current_time
                event.callback(*args if args else ())