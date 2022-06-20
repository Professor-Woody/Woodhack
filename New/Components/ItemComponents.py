from ecstremity import Component
from Components.Components import Position, Target, Stats, Initiative

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
                    if attackRoll >= target[Stats].defence:
                        damageRoll = sum([randint(1, self.diceType) for dice in range(self.diceAmount)]) + parentEntity[Stats].bonusDamage + self.bonusDamage
                        target.fire_event('damage', {'damage': damageRoll})
                    parentEntity[Initiative].speed += self.speed
                    self.entity[Initiative].speed += self.speed + 1

        

@dataclass
class UseFlashlight(Component):
    on = True

    def on_use(self, event):
        self.on = not self.on
        self.entity[Light].radius = self.entity[Light].baseRadius * int(self.on)
        
