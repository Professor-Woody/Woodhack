class Action:
    def __init__(self):
        pass
    def perform(self):
        print (f"why are you performing {type(self)}?")

class QuitAction(Action):
    def perform(self):
        print ("Quitting")
        raise SystemExit()

class PrintAction(Action):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def perform(self):
        print (self.msg)
        