from Components.Components import Position
from Components.UIComponents import Target
from Actions.EffectsActions import KillAction
class SubSystem:
    def __init__(self, system):
        self.system = system
        self.system.register(KillAction, self)

    def run(self, action):
        entity = action.entity

        targeters = entity[Position].level.world.create_query(all_of=['Target']).result
        for targeter in targeters:
            if targeter[Target].target == entity:
                targeter[Target].target = None
        entity.destroy()