from Actions.MoveActions import MovementAction
from Actions.UIActions import OpenSelectionUIAction, SelectionUISwapEquippedAction
from Systems.InventorySystem import InventorySystem
from Systems.RenderSystem import RenderSystem
from Systems.UpdateSystem import UpdateSystem
from Systems.MoveSystem import MoveSystem
from Systems.UseSystem import UseSystem
from Systems.DecideActionSystem import DecideActionSystem
from Systems.UISystem import TargetSystem, UISystem

from Actions.BaseActions import MoveAction
from Actions.UseActions import UseAction
from Actions.TargetActions import GetTargetAction
from Actions.InventoryActions import PickupItemAction

moveActions = [MoveAction, MovementAction]
targetActions = [GetTargetAction]
uiActions = [OpenSelectionUIAction, SelectionUISwapEquippedAction]
useActions = [UseAction]
inventoryActions = [PickupItemAction]

class SystemsManager:
    def __init__(self, level):
        self.level = level

        self.renderSystem = RenderSystem(self)
        self.updateSystem = UpdateSystem(self)
        self.decideActionSystem = DecideActionSystem(self)
        self.targetSystem = TargetSystem(self)
        self.moveSystem = MoveSystem(self)
        self.useSystem = UseSystem(self)
        self.uiSystem = UISystem(self)
        self.inventorySystem = InventorySystem(self)

    def post(self, action):
        print (action)
        if type(action) == list:
            for a in action:
                self.post(a)

        if type(action) in moveActions:
            self.moveSystem.post(action)
            print ("moveaction")
        elif type(action) in targetActions:
            self.targetSystem.post(action)
            print ("targetaction")
        elif type(action) in useActions:
            self.useSystem.post(action)
            print ("useaction")
        elif type(action) in uiActions:
            self.uiSystem.post(action)
        elif type(action) in inventoryActions:
            self.inventorySystem.post(action)

    def runSystems(self):
        # do the base updates for anything that needs updating
        self.updateSystem.run()
        
        # for anything that's now ready, find out if it's performing an action
        self.decideActionSystem.run()
        
        # now perform the actions
        self.inventorySystem.run()
        self.moveSystem.run()
        self.targetSystem.run()
        self.useSystem.run()

        # and draw
        self.renderSystem.run()
