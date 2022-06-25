from ecstremity import Component
from Components.Components import Position, Stats, Initiative, Light
from Components.UIComponents import Target
from Components.FlagComponents import IsReady
from random import randint
from dataclasses import dataclass

@dataclass
class UseMelee(Component):
    attack: int = 0
    diceType: int = 6
    diceAmount: int = 1
    bonusDamage: int = 0
    speed: int = 10


    def on_use(self, event):
        # perform a melee attack
        
        # check if melee attack
        # check if target
        # target in range
        # roll to hit
        # roll damage

        parentEntity = event.data.parentEntity
        target = parentEntity[Target].target

        if event.data.useType == 'meleeattack':
            if target:
                if Position.getRange(parentEntity, target) <= 1:
                    attackRoll = randint(-9, 10) + parentEntity[Stats].attack + self.attack
                    print (f"{parentEntity['Render'].entityName} is attacking {target['Render'].entityName}\n{parentEntity['Render'].entityName} rolled {attackRoll} to hit")

                    if attackRoll >= target[Stats].defence:
                        damageRoll = sum([randint(1, self.diceType) for dice in range(self.diceAmount)]) + parentEntity[Stats].bonusDamage + self.bonusDamage
                        target.fire_event('damage', {'damage': damageRoll})
                        print (f"{parentEntity['Render'].entityName} rolled {damageRoll} damage")
                    parentEntity[Initiative].speed += self.speed
                    self.entity[Initiative].speed += self.speed + 1
                    if parentEntity.has(IsReady):
                        parentEntity.remove(IsReady)
                    if self.entity.has(IsReady):
                        self.entity.remove(IsReady)

        
class UseFlashlight(Component):
    def __init__(self, on=True, radius=3):
        self.on = on
        if not self.entity.has(Light):
            self.entity.add(Light, {'radius': radius})
        self.setLight()

    def on_use(self, event):
        self.on = not self.on
        self.setLight()
        event.parentEntity.fire_event('recalculate_stats')

    def on_equip(self, event):
        event.parentEntity.fire_event('recalculate_stats')

    def setLight(self):
        self.entity[Light].radius = self.entity[Light].baseRadius * int(self.on)


@dataclass        
class AmuletOfYendor(Component):
    maxHp: int = 5

    def on_try_recalculate_stats(self, event):
        event.data.stats['maxHp'] += self.maxHp