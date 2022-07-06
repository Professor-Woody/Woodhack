from Actions.UseActions import DamageAction
from Actions.EffectsActions import KillAction
from Components.Components import Render, Stats
from ecstremity import Entity

class SubSystem:
    def __init__(self, system):
        self.system = system
        system.register(DamageAction, self)

    def run(self, action: DamageAction):
        print ("---Checking Damage---")
        
        entity = action.entity
        target: Entity = action.target
        damage = action.damage

        print (target[Stats].hp)
        print (damage)
        target[Stats].hp -= damage
        if target[Stats].hp <= 0:
            # target is dead
            print (f"{target[Render].entityName} has been killed")
            self.system.systemsManager.post(KillAction(target))