import tcod
from Actions.BaseActions import Action
from Screen import Screen
import Helpers.PositionHelper as PositionHelper
import Colours as colour
# in our program we will want entities
#   entities are nothing more than an ID number
# we will also have components
#   each component is just a dictionary of information
#   we will need a table for each component
#       the table has a primary key of the entity ID number, then values for each of the component parts
# 
# we will have a system for each action that can be taken
#   this will collect actions throughout the gameloop
#   each system is responsible for 1 action (though we can potentially group them together in)
#   the actions should contain nothing more than a reference to the entity ID
#   the system will iterate over all the entities that have flagged they need to do something

class MotionAction(Action):
    def __init__(self, app, event: tcod.event.MouseMotion):
        self.app = app
        self.pos = event.tile

    def perform(self):
        line = PositionHelper.getAngleLine(
            (self.app.x, self.app.y),
            # (self.pos.x, self.pos.y),
            (int(self.app.x * (-1 * 10)), int(self.app.y * int(.5*10))),
            10
        )
        for pos in line:
            self.app.screen.draw(pos[0], pos[1], ' ', bg=colour.RED)



class EvHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()

    def ev_mousemotion(self, event: tcod.event.MouseMotion):       
        self.app.screen.context.convert_event(event)
        return MotionAction(self.app, event)


class App:
    def __init__(self):
        self.width = 100
        self.height = 80

        self.isRunning = True

        self.x = 30
        self.y = 30

        self.mousex = 0
        self.mousey = 0

        evHandler = EvHandler(self)

        self.screen = Screen(self.width, self.height)

    
        while self.isRunning:
            self.screen.clear()
            for event in tcod.event.get():
                action = evHandler.dispatch(event)
                if action:
                    action.perform()
                
            self.screen.draw(self.x, self.y, "@")
            self.screen.flip()

a = App()