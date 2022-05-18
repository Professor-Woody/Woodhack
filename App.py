import tcod
from EventHandlers import EventHandler
from Level import Level
from Screen import Screen

class App:
    def __init__(self):
        self.screen = Screen(80, 50)  
        self.eventHandler = EventHandler() 
        self.isRunning = True    
        self.level = Level(self, 80, 50)

    def run(self):
        while self.isRunning:
            self.screen.clear()

            # handle events
            for event in tcod.event.get():
                action = self.eventHandler.dispatch(event)
                
                if action:
                    action.perform(self.level)
                            
            # update
            self.level.update()

            # draw
            self.level.draw(self.screen)
            self.screen.flip()



if __name__ == "__main__":
    app = App()
    app.run()

