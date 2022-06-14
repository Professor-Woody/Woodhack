from dataclasses import dataclass
from ecstremity import Component

class Melee(Component):
    pass

class Ranged(Component):
    pass

class Defence(Component):
    pass

@dataclass
class Use(Component):
    actions: list
