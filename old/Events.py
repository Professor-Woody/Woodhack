class Event:
    pass

class KeyDownEvent(Event):
    def __init__(self, key):
        Event.__init__(self)
        self.key = key

class KeyUpEvent(Event):
    def __init__(self, key):
        Event.__init__(self)
        self.key = key