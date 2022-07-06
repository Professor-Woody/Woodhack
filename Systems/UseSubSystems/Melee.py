from Actions.UseActions import UseAction, MeleeAction, DamageAction
from Components.Components import Initiative, Position, Stats
from Components.FlagComponents import IsReady
from Components.ItemComponents import UseMelee
from Components.UIComponents import Target
from random import randint

class SubSystem:
    def __init__(self, system):
        self.system = system
        system.register(MeleeAction, self)

    def run(self, action: MeleeAction):
        entity = action.entity
        item = action.item
        target = entity[Target].target
        
        if target:
            print ("===Performing melee attack===")

            if Position.getRange(entity, target) <= 1:
                attackRoll = randint(-9, 10) + entity[Stats].attack + item[UseMelee].attack
                print (f"{entity['Render'].entityName} is attacking {target['Render'].entityName}\n{entity['Render'].entityName} rolled {attackRoll} to hit")

                if attackRoll >= target[Stats].defence:
                    damageRoll = sum([randint(1, item[UseMelee].diceType) for dice in range(item[UseMelee].diceAmount)]) + entity[Stats].bonusDamage + item[UseMelee].bonusDamage
                    self.system.systemsManager.post(DamageAction(entity, target, damageRoll))
                    print (f"{entity['Render'].entityName} rolled {damageRoll} damage")
                entity[Initiative].speed += item[UseMelee].speed
                item[Initiative].speed += item[UseMelee].speed + 1
                self.system.systemsManager.post(UseAction(target, item))
                if entity.has(IsReady):
                    entity.remove(IsReady)
                if item.has(IsReady):
                    item.remove(IsReady)

