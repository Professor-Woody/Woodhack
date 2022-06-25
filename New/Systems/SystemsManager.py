from Actions.MoveActions import MovementAction
from Systems.RenderSystem import RenderSystem
from Systems.UpdateSystem import UpdateSystem
from Systems.MoveSystem import MoveSystem
from Systems.UseSystem import UseSystem
from Systems.DecideActionSystem import DecideActionSystem
from Systems.UISystem import TargetSystem

from Actions.BaseActions import MoveAction
from Actions.UseActions import UseAction
from Actions.TargetActions import GetTargetAction

moveActions = [MoveAction, MovementAction]
targetActions = [GetTargetAction]
useActions = [UseAction]

class SystemsManager:
    def __init__(self, level):
        self.level = level

        self.renderSystem = RenderSystem(self)
        self.updateSystem = UpdateSystem(self)
        self.decideActionSystem = DecideActionSystem(self)
        self.targetSystem = TargetSystem(self)
        self.moveSystem = MoveSystem(self)
        self.useSystem = UseSystem(self)
        

    def post(self, action):
        print (action)
        if type(action) in moveActions:
            self.moveSystem.post(action)
            print ("moveaction")
        elif type(action) in targetActions:
            self.targetSystem.post(action)
            print ("targetaction")
        elif type(action) in useActions:
            self.useSystem.post(action)
            print ("useaction")


    def runSystems(self):
        # do the base updates for anything that needs updating
        self.updateSystem.run()
        
        # for anything that's now ready, find out if it's performing an action
        self.decideActionSystem.run()
        
        # now perform the actions
        self.moveSystem.run()
        self.targetSystem.run()
        self.useSystem.run()

        # and draw
        self.renderSystem.run()
