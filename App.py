import tcod
from ecstremity import Engine
from EventHandler import EventHandler
from Levels.Level import GameLevel
from Screen import Screen
from Clock import Clock
from Levels.Level import GameLevel
from Components.Components import registerComponents
from Flags import FPS

class App:
    width = 150
    height = 100
    previousLevel = None

    def __init__(self):
        self.screen = Screen(self.width, self.height)
        self.eventHandler = EventHandler(self)
        self.isRunning = True

        self.ecs = Engine()
        self.entityDefs = {}
        registerComponents(self.ecs)

        self.level = GameLevel(self, self.width, self.height)
        self.clock = Clock(FPS)




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
            
            # update
            self.level.update()

            #draw
            self.level.draw(self.screen)
            self.screen.flip()

        
if __name__ == "__main__":
    app = App()
    app.run()