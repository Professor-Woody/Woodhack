from ecstremity import Component

class Target(Component):
    target = None

class Targeted(Component):
    def __init__(self):
        self.targetedBy = []
        self.targetIndex = 0
        self.cooldown = 0


class SelectionWindow(Component):
    pass