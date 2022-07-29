import tcod
from EventHandler import EventHandler
from Screen import Screen
from Clock import Clock
from Levels.BaseLevel import TestLevel
from Levels.OptionsLevel import OptionsLevel
from Levels.CharacterSelectLevel import CharacterSelectLevel
from Levels.MainMenu import MainMenu
from Flags import FPS


class App:
    width = 70
    height = 60
    previousLevel = None
    levelTemplates = {
        'MainMenu': MainMenu,    
        'CharacterSelect': CharacterSelectLevel,
        'Options': OptionsLevel
    }


    def __init__(self):
        self.screen = Screen(self.width, self.height)
        self.entityDefs = {}
        self.eventHandler = EventHandler(self)
        self.isRunning = True

        # self.level = TestLevel(self, self.width, self.height)
        self.level = MainMenu(self, self.width, self.height)
        self.clock = Clock(FPS)



    def run(self):
        while self.isRunning:
            # framerate
            self.clock.tick()
            # clear screen
            # self.screen.clear()

            # check for global/input events
            for event in tcod.event.get():
                action = self.eventHandler.dispatch(event)
                if action:
                    action.perform()
            # eventually loop this through each level too when we have
            # multiple levels
            self.level.update()

            self.screen.flip()

    def changeLevel(self, level):
        # We should probably power down the current level first.  TODO!

        self.screen.clear()
        self.level = self.levelTemplates[level](self, self.width, self.height)    
        

        
if __name__ == "__main__":
    app = App()
    app.run()