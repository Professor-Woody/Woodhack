from Actions.BaseActions import EntityAction
from dataclasses import dataclass
from ecstremity import entity

from ecstremity.entity import Entity

class OpenSelectionUIAction(EntityAction):
    def __init__(self, entity, selectionList, actions):
        super().__init__(entity)
        self.selectionList = selectionList
        self.actions = actions


class UpdateUIInputAction(EntityAction):
    pass


class CloseSelectionUIAction(EntityAction):
    pass

class SelectionUISwapEquippedAction(EntityAction):
    def __init__(self, entity, slot):
        super().__init__(entity)
        self.slot = slot

class UseItemInInventoryAction(EntityAction):
    pass

@dataclass
class SwapEquippedAction(EntityAction):
    entity: Entity
    slot: str
    item: Entity