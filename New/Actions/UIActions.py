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
    selectionUI: any = None


class SelectionUISwapEquippedAction(EntityAction):
    selectionUI: any = None
    def __init__(self, entity, slot):
        super().__init__(entity)
        self.slot = slot

class UseItemInInventoryAction(EntityAction):
    selectionUI: any = None

@dataclass
class SwapEquippedAction(EntityAction):
    slot: str
    item: Entity