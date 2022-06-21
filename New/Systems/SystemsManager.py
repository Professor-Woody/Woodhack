from Systems.RenderSystem import RenderSystem
from Systems.UpdateSystem import UpdateSystem
from Systems.MoveSystem import MoveSystem
from Systems.UseSystem import UseSystem
from Systems.DecideActionSystem import DecideActionSystem
from Systems.UISystem import TargetSystem

from Actions.BaseActions import MoveAction, TargetAction

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
        if type(action) == MoveAction:
            self.moveSystem.post(action)
        elif type(action) == TargetAction:
            self.targetSystem.post(action)
        elif type(action) == UseAction:
            self.useSystem.post(action)


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
