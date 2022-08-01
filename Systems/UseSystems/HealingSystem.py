from Components import UseHealing, Stats, Target
from Systems.BaseSystem import BaseSystem
import Helpers.Dice as dice

class HealingSystem(BaseSystem):
    actions = ['use_healing']
    alwaysActive = False

    def run(self):
        healComponents = self.getComponents(UseHealing)
        statComponents = self.getComponents(Stats)
        targetComponents = self.getComponents(Target)

        for action in self.actionQueue:
            entity = action['entity']
            target = targetComponents[action['parentEntity']]['target']
            if not target:
                target = action['parentEntity']

                                    # amount, type, modifier
            healingAmount = dice.roll(healComponents[entity]['diceAmount'], healComponents[entity]['diceType'], healComponents[entity]['modifier'])
            statComponents[target]['hp'] = min(statComponents[target]['hp']+healingAmount, statComponents[target]['maxHp'])
            
            self.level.post('add_speed', {'entity': action['parentEntity'], 'speed': healComponents[entity]['moveSpeed']})
            self.level.post('add_speed', {'entity': entity, 'speed': healComponents[entity]['itemSpeed']})
            self.log(f"£{target}$ was healed for {healingAmount} points")