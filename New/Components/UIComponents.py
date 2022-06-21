from ecstremity import Component

class Target(Component):
    target = None

class Targeted(Component):
    def __init__(self):
        self.targetedBy = set()