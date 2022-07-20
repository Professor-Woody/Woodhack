from Systems.BaseSystem import BaseSystem
from Components import *

class RecalculateStatsSystem(BaseSystem):
    actions = ['recalculate_stats']

    def run(self):
        if self._actionQueue:
            statsComponents = self.getComponents(Stats)
            statModifierComponents = self.getComponents(StatModifier)
            lightComponents = self.getComponents(Light)
            bodyComponents = self.getComponents(Body)

            for action in self.actionQueue:
                entity = action['entity']
                print (f"Recalculating stats for {entity}")
                statsComponents[entity]['hp'] = statsComponents[entity]['baseMaxHp'] + statsComponents[entity]['maxHp'] - statsComponents[entity]['hp']
                statsComponents[entity]['attack'] = statsComponents[entity]['baseAttack']
                statsComponents[entity]['defence'] = statsComponents[entity]['baseDefence']
                statsComponents[entity]['moveSpeed'] = statsComponents[entity]['baseMoveSpeed']
                lightRadius = 0

                for slot in bodyComponents[entity].keys():
                    if bodyComponents[entity][slot]:
                        if self.level.e.hasComponent(bodyComponents[entity][slot], StatModifier):
                            for key, value in statModifierComponents[bodyComponents[entity][slot]].items():
                                statsComponents[entity][key] += value

                        if self.level.e.hasComponent(bodyComponents[entity][slot], Light):
                            radius = lightComponents[bodyComponents[entity][slot]]['radius']
                            if radius > lightRadius:
                                lightRadius = radius
                
                if statsComponents[entity]['hp'] < 1:
                    statsComponents[entity]['hp'] = 1
                if statsComponents[entity]['moveSpeed'] < 6:
                    statsComponents[entity]['moveSpeed'] = 6
                if not self.level.e.hasComponent(entity, Light):
                    if lightRadius > 0:
                        self.level.e.addComponent(entity, Light, {'radius': lightRadius})
                else:
                    if lightRadius > 0:
                        lightComponents[entity]['radius'] = lightRadius
                    else:
                        self.level.e.removeComponent(entity, Light)

                print ("Recalculation finished")
                print (f"Stats:\n{statsComponents[entity]}")
            

