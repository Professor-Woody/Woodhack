import tcod
from EventHandler import EventHandler
from Screen import Screen
from Controllers import KeyboardController
from Clock import Clock


class App:
    width = 150
    height = 100

    def __init__(self):
        self.screen = Screen(self.width, self.height)
        self.eventHandler = EventHandler(self)
        self.isRunning = True

        self.level = MainMenu(self, self.width, self.height)
        self.clock = Clock(60)


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

        