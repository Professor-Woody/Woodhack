from Actions.EffectsActions import RecalculateStatsAction
from Actions.MoveActions import MovementAction
from Actions.UIActions import CloseSelectionUIAction, OpenSelectionUIAction, SelectionUISwapEquippedAction, SwapEquippedAction, UpdateUIInputAction
from Systems.InventorySystem import InventorySystem
from Systems.RenderSystem import RenderSystem
from Systems.UpdateSystem import UpdateSystem
from Systems.MoveSystem import MoveSystem
from Systems.UseSystem import UseSystem
from Systems.DecideActionSystem import DecideActionSystem
from Systems.UISystem import TargetSystem, UISystem
from Systems.EffectsSystem import EffectsSystem

from Actions.BaseActions import MoveAction, UpdateLightingAction
from Actions.UseActions import UseAction, MeleeAction
from Actions.TargetActions import GetTargetAction
from Actions.InventoryActions import PickupItemAction

moveActions = [MoveAction, MovementAction]
updateActions = [UpdateLightingAction]
targetActions = [GetTargetAction]
uiActions = [OpenSelectionUIAction, SelectionUISwapEquippedAction, UpdateUIInputAction, CloseSelectionUIAction]
useActions = [UseAction, MeleeAction]
inventoryActions = [PickupItemAction, SwapEquippedAction]
effectsActions = [RecalculateStatsAction]

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
        self.effectsSystem = EffectsSystem(self)

    def post(self, action):
        if type(action) is not UpdateUIInputAction:
            print (action)
        if type(action) == list:
            for a in action:
                self.post(a)

        elif type(action) in moveActions:
            self.moveSystem.post(action)
        elif type(action) in targetActions:
            self.targetSystem.post(action)
        elif type(action) in useActions:
            self.useSystem.post(action)
        elif type(action) in uiActions:
            self.uiSystem.post(action)
        elif type(action) in inventoryActions:
            self.inventorySystem.post(action)
        elif type(action) in updateActions:
            self.updateSystem.post(action)
        elif type(action) in effectsActions:
            print (f"posting {action} to effectsSystem")
            self.effectsSystem.post(action)

    def runSystems(self):
        # do the base updates for anything that needs updating
        self.moveSystem.run()
        self.updateSystem.run()
        
        # for anything that's now ready, find out if it's performing an action
        self.decideActionSystem.run()
        
        # now perform the actions
        self.inventorySystem.run()
        self.targetSystem.run()
        self.uiSystem.run()
        self.useSystem.run()
        self.effectsSystem.run()

        # and draw
        self.renderSystem.run()
