from dataclasses import dataclass
from ecstremity import Component
from Actions.EntityActions import RangedAttackAction

@dataclass
class IsEquipped(Component):
    parentEntity: Entity


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
    
    def __init__(self, attack, attackSpeed, damageBonus, diceAmount, diceType, ammoType):
        self.attack = attack
        self.attackSpeed = attackSpeed
        self.damageBonus = damageBonus
        self.diceAmount = diceAmount
        self.diceType = diceType
        self.ammoType = ammoType
        
        self.entity['Use'].addAction(RangedAttackAction)

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

class Use(Component):
    actions: list
    cancelUse: bool = False
    destroyAfterUse: bool

    def __init__(self, actions=[], destroyAfterUse=False):
        self.actions = actions
        self.destroyAfterUse = destroyAfterUse
    

    def addAction(self, action):
        actions.append(action(self))

    def on_use(self, event):
        for action in self.actions:
            action.perform()
            if self.cancelUse:
                self.cancelUse = False
                break

        if self.destroyAfterUse:
            self.entity.remove(self.entity)