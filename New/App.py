import tcod
from Systems.RenderSystem import RenderSystem
from Systems.UpdateSystem import UpdateSystem
from ecstremity import Engine
from EventHandler import EventHandler
from Levels.Level import GameLevel
from Screen import Screen
from Clock import Clock
from Levels.Level import GameLevel
from Components.ComponentRegister import registerComponents
from Flags import FPS
import os

class App:
    width = 100
    height = 80
    previousLevel = None

    def __init__(self):
        print ("------------")
        print (os.getcwd())

        self.screen = Screen(self.width, self.height)
        self.eventHandler = EventHandler(self)
        self.isRunning = True

        self.ecs = Engine()
        self.entityDefs = {}
        registerComponents(self.ecs)

        self.level = GameLevel(self, self.width, self.height)
        self.clock = Clock(FPS)

        self.systems = set()
        self.systems.add(RenderSystem())
        self.systems.add(UpdateSystem())

    def run(self):
        while self.isRunning:
            # framerate
            self.clock.tick()
            # clear screen
            self.screen.clear()

            # check for global/input events
            for event in tcod.event.get():
                action = self.eventHandler.dispatch(event)
                if action:
                    action.perform()
            # eventually loop this through each level too when we have
            # multiple levels
            for system in self.systems:
                system.run(level=self.level)

            self.screen.flip()

    
        
if __name__ == "__main__":
    app = App()
    app.run()