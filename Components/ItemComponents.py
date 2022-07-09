from dataclasses import dataclass
from ecstremity import Component
from Components.Components import Position, Stats
from Components.TargetComponents import Target
from Components.FlagComponents import IsEquipped, IsReady
from random import randint
@dataclass
class Melee(Component):
    attack: int = 0
    userSpeed: int = 30
    readySpeed: int = 45
    diceType: int = 6
    diceAmount: int = 1
    bonusDamage: int = 0
    weaponRange: int = 1

    def on_melee(self, action):
        print ("in on_melee")
        parentEntity = action.data.parentEntity
        target = action.data.target
        print (1)

        if Position.getRange(parentEntity, target) <= self.weaponRange:
            print (2)
            attackRoll = randint(-9, 10) + parentEntity[Stats].attack + self.attack
            print (3)
            print (f"{parentEntity['Render'].entityName} is attacking {target['Render'].entityName}\n{self.entity['Render'].entityName} rolled {attackRoll} to hit")
            
            if attackRoll >= target[Stats].defence:
                damageRoll = sum([randint(1, self.diceType) for dice in range(self.diceAmount)]) + parentEntity[Stats].bonusDamage + self.bonusDamage
                self.entity.fire_event('use', {'parentEntity': parentEntity})
                target.fire_event('damage', {'damage': damageRoll})
                
                print (f"{self.entity['Render'].entityName} rolled {damageRoll} damage")
            parentEntity.fire_event('add_speed', {'speed': self.userSpeed})
            self.entity.fire_event('add_speed', {'speed': self.readySpeed + randint(1, 200)})
            


