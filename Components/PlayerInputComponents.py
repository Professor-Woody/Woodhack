from Components.ItemComponents import Melee
from Components.TargetComponents import Target
from ecstremity import Component
from Components.FlagComponents import IsMelee, IsReady
from Components.Components import Position, Stats
from ecstremity.entity_event import ECSEvent

class PlayerInput(Component):
    def __init__(self, controller = None):
        self.controller = controller
        self.controlFocus = []

    def on_update(self, action):
        self.controller.update()
        if self.controlFocus:
            return
            
        target = None
        if self.controller.getPressedOnce("next"):
            target = "next"
        elif self.controller.getPressedOnce("previous"):
            target = "previous"
        # elif self.controller.getPressedOnce("nearestEnemy"):
        #     target = "nearestEnemy"
        if target:
            print (f"attempting to target {target}")
            # self.entity.fire_event('set_target', {'targetSelectionOrder': target, 'targetType': 'NPC'})
            self.entity.post(ECSEvent('set_target', {'targetSelectionOrder': target, 'targetType': 'NPC'}))

        if self.controller.getPressedOnce("use"):
            # self.entity.fire_event("pickup_item", {'position': self.entity[Position]})
            self.entity.post(ECSEvent('pickup_item', {'position': self.entity[Position]}))

        if self.controller.getPressedOnce("inventory"):
            # self.entity.fire_event("open_inventory")
            self.entity.post(ECSEvent('open_inventory'))
            return

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
                # self.entity.fire_event('move', {'dx': dx, 'dy': dy})
                self.entity.post(ECSEvent('move', {'dx': dx, 'dy': dy}))
                # self.entity.fire_event('add_speed', {'speed': self.entity[Stats].moveSpeed})
                self.entity.post(ECSEvent('add_speed', {'speed': self.entity[Stats].moveSpeed}))
                return

# check melee
            meleed = False
            hands = ['lefthand', 'righthand']
            for hand in hands:
                item = self.entity['Body'].slots[hand] 
                if item and item.has(Melee) and item.has(IsReady):
                    if self.entity[Target].target and Position.getRange(self.entity, self.entity[Target].target) <= item[Melee].weaponRange:
                        # item.fire_event('melee', {'parentEntity': self.entity, 'target': self.entity[Target].target})
                        print ("meleeing")
                        item.post(ECSEvent('melee', {'parentEntity': self.entity}))
                        meleed = True
            if meleed:
                return

            # check use
            for hand in hands:
                if self.controller.getPressedOnce(hand):
                    item = self.entity['Body'].slots[hand] 
                    if item and item.has(IsReady):
                        # item.fire_event('use', {'parentEntity': self.entity})
                        item.post(ECSEvent('use', {'parentEntity': self.entity}))
                        return



            if self.controller.getPressedOnce('cancel'):
                self.entity[Position].level.entityManager.spawn('orc', self.entity[Position].x+1, self.entity[Position].y)
            if self.controller.getPressedOnce('nearestEnemy'):
                self.entity[Position].level.entityManager.spawn('torch', self.entity[Position].x-1, self.entity[Position].y)