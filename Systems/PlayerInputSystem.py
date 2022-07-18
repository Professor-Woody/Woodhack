from Systems.BaseSystem import BaseSystem
from Components import *

class PlayerInputSystem(BaseSystem):
    def run(self):
        entities = self.level.playersQuery.result
        inputComponents = self.level.e.component.filter(PlayerInput, entities)

        for entity in entities:
            controller = inputComponents[entity]['controller']
            controller.update()

            # Targeting
            target = None
            if controller.getPressedOnce("next"):
                target = "next"
            elif controller.getPressedOnce("previous"):
                target = "previous"
            elif controller.getPressedOnce("nearestEnemy"):
                target = "nearestEnemy"
            if target:
                self.level.post('target', {'entity': entity, 'targetType': IsNPC, 'targetFocus': target})

            # picking up an item
            if controller.getPressedOnce("use"):
                self.level.post('try_pickup_item', {'entity': entity})

            # Movement
            if self.level.e.hasComponent(entity, IsReady):
                dx = 0
                dy = 0
                if controller.getPressed("up"):
                    dy -= 1
                if controller.getPressed("down"):
                    dy += 1
                if controller.getPressed("left"):
                    dx -= 1
                if controller.getPressed("right"):
                    dx += 1

                if dx or dy:
                    self.level.post('move', {'entity': entity, 'dx': dx, 'dy': dy})
                    self.level.post('add_speed', {'entity': entity, 'speed': 6})
                    return




        