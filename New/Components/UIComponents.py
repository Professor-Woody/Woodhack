from ecstremity import Component
from ecstremity import Entity

class Target(Component):
    target = None

class Targeted(Component):
    def __init__(self):
        self.targetedBy = []
        self.targetIndex = 0
        self.cooldown = 0



class SelectionWindowUI(Component):
    def __init__(self, parentEntity, selectionList, actions):
        self.parentEntity: Entity = parentEntity
        self.selectionList: list = selectionList
        self.selectionIndex: int = 0
        self.actions: list = actions



