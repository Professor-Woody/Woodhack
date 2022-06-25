from Systems.BaseSystem import BaseSystem
from Components.Components import Position, Stats, PlayerInput, Body
from Components.FlagComponents import IsReady, IsMelee
from Actions.TargetActions import GetTargetAction
from Actions.MoveActions import MovementAction
from Components.UIComponents import Target
from Actions.UseActions import UseAction

class DecideActionSystem(BaseSystem):
    def run(self):
        self.runPlayerActions()
        self.runNPCActions()



    def runNPCActions(self):
        pass



    def runPlayerActions(self):
        entities = self.level.world.create_query(all_of=['IsPlayer', 'IsReady']).result
        
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
                self.systemsManager.post(GetTargetAction(entity, "NPC", target))

            #  ----------------------
            # check if they attempt to pick something up or open their inventory



            #  ----------------------
            # don't allow them to do anything else unless they are ready to
            if not entity.has(IsReady):
                continue
            #  ----------------------
            # check movement
            dx = 0
            dy = 0
            if entity[PlayerInput].controller.getPressed("up"):
                dy -= 1
            if entity[PlayerInput].controller.getPressed("down"):
                dy += 1
            if entity[PlayerInput].controller.getPressed("left"):
                dx -= 1
            if entity[PlayerInput].controller.getPressed("right"):
                dx += 1

            if dx or dy:
                self.systemsManager.post(MovementAction(entity, dx, dy, entity[Stats].moveSpeed))
                return
            

            # check melee
            meleed = False
            hands = ['lefthand', 'righthand']
            for hand in hands:
                item = entity[Body].slots[hand] 
                if item and item.has(IsMelee) and item.has(IsReady):
                    if entity[Target].target and Position.getRange(entity, entity[Target].target) <= 1:
                        self.systemsManager.post(UseAction(item, 'meleeattack', entity))
                        meleed = True
            if meleed:
                return

            # check use
            for hand in hands:
                if entity[PlayerInput].controller.getPressed(hand):
                    item = entity[Body].slots[hand] 
                    if item and item.has(IsReady):
                        self.systemsManager.post(UseAction(item, 'trigger', entity))
                        return
        # print ("decideaction end")