from Systems.BaseSystem import BaseSystem
from Components import *
import Helpers.PositionHelper as PositionHelper

class PlayerInputSystem(BaseSystem):
    priority = 10
    
    def run(self):
        entities = self.level.playersQuery.result
        inputComponents = self.level.e.component.filter(PlayerInput, entities)
        statsComponents = self.level.e.component.filter(Stats, entities)
        targetComponents = self.level.e.component.filter(Target, entities)
        bodyComponents = self.getComponents(Body)
        positionComponents = self.getComponents(Position)
        weaponComponents = self.getComponents(WeaponStats)
        useActionComponents = self.getComponents(UseActions)

        for entity in entities:
            controller = inputComponents[entity]['controller']
            controller.update()

            if inputComponents[entity]['controlFocus']:
                continue
            
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

            
            if self.level.e.hasComponent(entity, IsReady):
                # Movement
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
                    self.level.post('add_speed', {'entity': entity, 'speed': statsComponents[entity]['moveSpeed']})
                    continue

                # inventory
                if controller.getPressedOnce('inventory'):
                    self.level.post('open_inventory', {'entity': entity})
                    self.level.lowestFps = 1000
                    continue

                # melee
                slots = ['mainhand', 'offhand']
                if targetComponents[entity]['target']:
                    
                    meleed = False

                    for slot in slots:
                        if bodyComponents[entity][slot] and \
                        self.level.e.hasComponent(bodyComponents[entity][slot], Melee) and \
                        self.level.e.hasComponent(bodyComponents[entity][slot], IsReady):                            
                            if PositionHelper.getRange(
                                (positionComponents[entity]['x'], positionComponents[entity]['y']),
                                (positionComponents[targetComponents[entity]['target']]['x'], positionComponents[targetComponents[entity]['target']]['y'])
                            ) <= weaponComponents[bodyComponents[entity][slot]]['range']:
                                self.level.post('melee', {'slot': slot, 'target': targetComponents[entity]['target'], 'entity': entity, 'item': bodyComponents[entity][slot]})
                                meleed = True
                    if meleed:
                        continue

                # use item in hand
                for slot in slots:
                    if controller.getPressed(slot) and \
                        bodyComponents[entity][slot] and \
                            self.level.e.hasComponent(bodyComponents[entity][slot], UseActions) and \
                                self.level.e.hasComponent(bodyComponents[entity][slot], IsReady):
                        for action in useActionComponents[bodyComponents[entity][slot]]['actions']:
                            self.level.post(action, {
                                'entity': bodyComponents[entity][slot],
                                'parentEntity': entity,
                                'command': slot
                            })


                # TODO: REMOVE THIS
                # Temporary for testing purposes
                if controller.getPressedOnce('cancel'):
                    self.level.e.spawn('orc', positionComponents[entity]['x']+1, positionComponents[entity]['y'])