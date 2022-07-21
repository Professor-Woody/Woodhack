from Components import *
from Systems.BaseSystem import BaseSystem
from random import randint

class MeleeSystem(BaseSystem):
    actions = ['melee']

    def run(self):
        if self._actionQueue:
            meleeComponents = self.getComponents(Melee)
            statsComponents = self.getComponents(Stats)
            

            for action in self.actionQueue:
                entity = action['entity']
                target = action['target']
                item = action['item']

                # roll attack
                attackRoll = randint(-9, 10) + statsComponents[entity]['attack'] + meleeComponents[item]['attack'] - statsComponents[target]['defence']
                print (f"{entity} attacks {target} with an attack roll of {attackRoll}")

                if attackRoll >= 0:
                    # roll damage
                    damageRoll = sum([randint(1, meleeComponents[item]['damageDiceType']) for dice in range(meleeComponents[item]['damageDiceAmount'])]) + meleeComponents[item]['damageBonus']
                    print (f"--{target} is damaged for {damageRoll} points")
                    # post damage
                    self.level.post('damage', {'entity': target, 'damage': damageRoll})
                self.level.post('add_speed', {'entity': entity, 'speed': meleeComponents[item]['moveSpeed']})
                self.level.post('add_speed', {'entity': item, 'speed': meleeComponents[item]['weaponSpeed']})


class DamageSystem(BaseSystem):
    actions = ['damage']

    def run(self):
        if self._actionQueue:
            statsComponents = self.getComponents(Stats)
            targetedComponents = self.getComponents(Targeted)
            targetComponents = self.getComponents(Target)

            for action in self.actionQueue:
                entity = action['entity']
                statsComponents[entity]['hp'] -= action['damage']
                if statsComponents[entity]['hp'] <= 0:
                    print (f"{entity} has died")
                    
                    if self.level.e.hasComponent(entity, IsPlayer):
                        self.level.post('add_speed', {'entity': entity, 'speed': 1000000})
                        return
                        
                    if self.level.e.hasComponent(entity, Targeted):
                        for targeter in targetedComponents[entity]['targetedBy']:
                            targetComponents[targeter]['target'] = None
                    
                    self.level.e.destroyEntity(entity)

