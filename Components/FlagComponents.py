from ecstremity import Component
from dataclasses import dataclass

class IsPlayer(Component):
    pass

class IsReady(Component):
    pass

class IsNPC(Component):
    pass

class IsItem(Component):
    pass

class IsMelee(Component):
    pass

class BlocksMovement(Component):
    pass

class IsUI(Component):
    pass

class IsEquippable(Component):
    def __init__(self, slots):
        # {"slotname": "actual_slotname"}
        self.slots = slots

class NeedsUpdate(Component):
    allow_multiple: bool = True

@dataclass
class IsEquipped(Component):
    slot: str
    parentEntity = None