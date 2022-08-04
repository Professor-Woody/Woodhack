from EventHandler import EventHandler
from Screen import Screen
import tcod
from Levels.LevelCreator import NewLevelCreator, loadTestData

class App:
    width = 140
    height = 100
    isRunning = True
    gameMap = None

    def __init__(self):
        self.screen = Screen(self.width, self.height)
        self.eventHandler = EventHandler(self, test=True)
        loadTestData()
        self.regenerateLevel()

    def run(self):
        while self.isRunning:
            for event in tcod.event.get():
                action = self.eventHandler.dispatch(event)
                if action:
                    action.perform()

            self.map.draw(self.screen)
            self.screen.draw(5, 5, "@")
            self.screen.flip()
    
    def regenerateLevel(self):
        self.screen.clear()
        self.screen.printLine(10, 10, "Generating Level...")
        self.screen.flip()
        self.map = NewLevelCreator.generateLevel(None, self.width, self.height, "caverns")
        self.map.visible[:] = True
        self.map.lit[:] = True

       
if __name__ == "__main__":
    app = App()
    app.run()