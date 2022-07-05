from Actions.UseActions import DamageAction
from Components.Components import Render, Stats
from ecstremity import Entity

class SubSystem:
    def __init__(self, system):
        self.system = system
        system.register(DamageAction, self)

    def run(self, action: DamageAction):
        entity = action.entity
        target: Entity = action.target
        damage = action.damage

        target[Stats].hp -= damage
        if target[Stats].hp <= 0:
            # target is dead
            print (f"{target[Render].entityName} has been killed")
            target.destroy()