from Systems.BaseSystem import BaseSystem
from Components.Components import Position, Stats, Initiative
from Components.FlagComponents import IsReady

class DecideActionSystem(BaseSystem):
    def run(self):
        # for each player
            # check inputs
            # dispatch actions to their event handlers to queue up


        entities = self.level.world.create_query(all_of=[IsPlayer, IsReady]).result
        
        for entity in entities:
            #  ----------------------
            # check targeting
            target = None
            if entity[PlayerInput].controller.getPressedOnce("next"):
                target = "next"
            elif entity[PlayerInput].controller.getPressedOnce("previous"):
                target = "previous"
            elif entity[PlayerInput].controller.getPressedOnce("nearestEnemy"):
                target = "nearestEnemy"
            if target:
                self.systemsManager.post(GetTargetAction(entity, "IsNPC", target))

            #  ----------------------
            # check if they attempt to pick something up or open their inventory


            #  ----------------------
            # check movement
            dx = 0
            dy = 0
            if self.entity[PlayerInput].controller.getPressed("up"):
                dy -= 1
            if self.entity[PlayerInput].controller.getPressed("down"):
                dy += 1
            if self.entity[PlayerInput].controller.getPressed("left"):
                dx -= 1
            if self.entity[PlayerInput].controller.getPressed("right"):
                dx += 1

            if dx or dy:
                self.systemsManager.post(MovementAction(entity[Position], dx, dy, entity[Stats].moveSpeed, entity[Initiative]))
                return
            

            # check melee
            meleed = False
            for hand in entity[Body].hands.keys():
                item = entity[Body].hands[hand] 
                if item and item.has(UseMelee) and item.has(IsReady):
                    if entity[Target].target and Position.getRange(entity, entity[Target].target) <= 1:
                        self.systemsManager.post(UseAction(item, 'meleeattack', entity))
                        meleed = True
            if meleed:
                return

            # check use
            for hand in entity[Body].hands.keys():
                if entity[PlayerInput].controller.getPressed(hand):
                    item = entity[Body].hands[hand] 
                    if item and item.has(IsReady):
                        self.systemsManager.post(UseAction(item, 'trigger', entity))
                        return