from ecstremity import Component
from Components.Components import Position, Stats, Initiative, Light
from Components.UIComponents import Target
from Components.FlagComponents import IsReady
from random import randint
from dataclasses import dataclass

class UseMelee(Component):
    def __init__(self, 
                attack = 0, 
                diceType = 6,
                diceAmount = 1,
                bonusDamage = 0,
                speed = 30):
        self.attack: int = attack
        self.diceType: int = diceType
        self.diceAmount: int = diceAmount
        self.bonusDamage: int = bonusDamage
        self.speed: int = speed

        
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