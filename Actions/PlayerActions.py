from Actions.Actions import EntityAction
from Actions.InventoryActions import OpenInventoryAction
from Actions.EntityActions import MovementAction, PickupItemAction, GetTargetAction


class GetPlayerInputAction(EntityAction):
    def perform(self):
            # check menu

            
            # check movement
            dx = 0
            dy = 0
            if self.entity['PlayerInput'].controller.getPressed("up"):
                dy -= 1
            if self.entity['PlayerInput'].controller.getPressed("down"):
                dy += 1
            if self.entity['PlayerInput'].controller.getPressed("left"):
                dx -= 1
            if self.entity['PlayerInput'].controller.getPressed("right"):
                dx += 1

            if dx or dy:
                MovementAction(self.entity['Position'], dx, dy, self.entity['Stats'].moveSpeed).perform()            

            # check use actions (IE equipment)
            if self.entity['PlayerInput'].controller.getPressedOnce('inventory'):
                OpenInventoryAction(self.entity).perform()
            if self.entity['PlayerInput'].controller.getPressedOnce('use'):
                PickupItemAction(self.entity).perform()
            # print (3)

            # check targetting
            target = None
            if self.entity['PlayerInput'].controller.getPressedOnce("next"):
                target = "next"
            elif self.entity['PlayerInput'].controller.getPressedOnce("previous"):
                target = "previous"
            elif self.entity['PlayerInput'].controller.getPressedOnce("nearestEnemy"):
                target = "nearestEnemy"
            # print (target)
            if target:
                GetTargetAction(self.entity, target).perform()
            # print (4)

