from Actions.BaseActions import EntityAction
from dataclasses import dataclass

from ecstremity.entity import Entity

class OpenSelectionUIAction(EntityAction):
    def __init__(self, entity, selectionList, actions):
        super().__init__(entity)
        self.selectionList = selectionList
        self.actions = actions

@dataclass
class UpdateUIInputAction(EntityAction):
    pass


@dataclass
class CloseSelectionUIAction(EntityAction):
    pass

@dataclass
class SelectionUISwapEquippedAction(EntityAction):
    slot: str

@dataclass
class UseItemInInventoryAction(EntityAction):
    pass

@dataclass
class SwapEquippedAction(EntityAction):
    slot: str
    item: Entity