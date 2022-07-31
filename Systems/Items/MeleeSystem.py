from Components import *
from Systems.BaseSystem import BaseSystem
from random import randint
import Colours as colour


class MeleeSystem(BaseSystem):
    actions = ['melee']

    def run(self):
        if self._actionQueue:
            weaponComponents = self.getComponents(WeaponStats)
            statsComponents = self.getComponents(Stats)
            

            for action in self.actionQueue:
                entity = action['entity']
                target = action['target']
                item = action['item']

                # roll attack
                attackRoll = randint(-9, 10) \
                    + statsComponents[entity]['attack'] \
                        + statsComponents[entity]['dex'] \
                            + weaponComponents[item]['attack'] \
                                - statsComponents[target]['defence']

                # print (f"{entity} attacks {target} with an attack roll of {attackRoll}")
                self.clog(f"£{entity}$ attacks £{target}$ with an attack roll of {attackRoll}")

                if attackRoll >= 0:
                    # roll damage
                    damageRoll = sum([randint(1, weaponComponents[item]['damageDiceType']) for dice in range(weaponComponents[item]['damageDiceAmount'])]) \
                        + weaponComponents[item]['damageBonus'] \
                            + statsComponents[entity]['str']
                    # print (f"--{target} is damaged for {damageRoll} points")
                    self.clog(f"£{target}$ is damaged for {damageRoll} points")
                    # post damage
                    self.level.post('damage', {'entity': target, 'damage': damageRoll})
                    
                self.level.post('add_speed', {'entity': entity, 'speed': weaponComponents[item]['moveSpeed']})
                self.level.post('add_speed', {'entity': item, 'speed': weaponComponents[item]['weaponSpeed']})


class DamageSystem(BaseSystem):
    actions = ['damage']

    def run(self):
        if self._actionQueue:
            statsComponents = self.getComponents(Stats)


            for action in self.actionQueue:
                entity = action['entity']
                statsComponents[entity]['hp'] -= action['damage']
                if statsComponents[entity]['hp'] <= 0:
                    print (f"{entity} has died")
                    self.clog(f"£{entity}$ has died", colour.RED)
                    self.level.post('entity_died', {'entity': entity})



class DeathSystem(BaseSystem):
    actions = ['entity_died']
    
    def run(self):
        if self._actionQueue:
            targetComponents = self.getComponents(Target)
            targetedComponents = self.getComponents(Targeted)

            for action in self.actionQueue:
                entity = action['entity']
                if self.level.e.hasComponent(entity, IsPlayer):
                    self.level.post('add_speed', {'entity': entity, 'speed': 1000000})
                    continue
                    
                if self.level.e.hasComponent(entity, Targeted):
                    for targeter in targetedComponents[entity]['targetedBy']:
                        targetComponents[targeter]['target'] = None
                
                self.level.e.destroyEntity(entity)

