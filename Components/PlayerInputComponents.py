from ecstremity import Component
from Components.FlagComponents import IsReady, NeedsUpdate


class PlayerInput(Component):
    def __init__(self, controller = None):
        self.controller = controller
        self.controlFocus = []

    def on_update(self, action):
        self.controller.update()

        target = None
        if self.controller.getPressedOnce("next"):
            target = "next"
        elif self.controller.getPressedOnce("previous"):
            target = "previous"
        elif self.controller.getPressedOnce("nearestEnemy"):
            target = "nearestEnemy"
        if target:
            print (f"attempting to target {target}")
            self.entity.fire_event('set_target', {'targetSelectionOrder': target, 'targetType': 'NPC'})


        if self.entity.has(IsReady):
            dx = 0
            dy = 0
            if self.controller.getPressed("up"):
                dy -= 1
            if self.controller.getPressed("down"):
                dy += 1
            if self.controller.getPressed("left"):
                dx -= 1
            if self.controller.getPressed("right"):
                dx += 1
            if dx or dy:
                self.entity.fire_event('move', {'dx': dx, 'dy': dy})
                self.entity.fire_event('add_speed', {'speed': 6})
                return
            
            if self.controller.getPressedOnce('use'):
                self.entity['Position'].level.entityManager.spawn('orc', self.entity['Position'].x+1, self.entity['Position'].y)
