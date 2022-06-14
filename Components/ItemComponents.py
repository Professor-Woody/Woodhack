from dataclasses import dataclass
from ecstremity import Component

@dataclass
class Melee(Component):
    attack: int
    attackSpeed: int
    damageBonus: int
    diceAmount: int
    diceType: int

class Ranged(Component):
    attack: int
    attackSpeed: int
    damageBonus: int
    diceAmount: int
    diceType: int
    ammoType: str

@dataclass
class Defence(Component):
    armour: int

@dataclass
class MoveSpeedModifier(Component):
    modifier: int

@dataclass
class AttackModifier(Component):
    modifier: int

@dataclass
class HPModifier(Component):
    modifier: int

@dataclass
class Use(Component):
    actions: list
    destroyAfterUse: bool = False