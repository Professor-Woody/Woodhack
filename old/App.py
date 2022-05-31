import tcod
from EventHandlers import EventHandler
from Level import Level
from Screen import Screen
from Controllers import KeyboardController
import time

class App:
    width = 192
    height = 108
    def __init__(self):
        self.screen = Screen(self.width, self.height)  
        self.eventHandler = EventHandler(self) 
        self.isRunning = True    
        self.keyboardController = KeyboardController()    # there's only 1 keyboard per computer    
        # self.level = Level(self, self.width, self.height)
        self.level = MainMenu(self, self.width, self.height)
        self.clock = Clock(60)

    def run(self):
        while self.isRunning:
            self.clock.tick()

            self.screen.clear()

            # handle events
            for event in tcod.event.get():
                action = self.eventHandler.dispatch(event)
                
                if action:
                    action.perform()
                            
            # update
            self.level.update()

            # draw
            self.level.draw(self.screen)
            self.screen.flip()


class Clock:
    def __init__(self, fps):
        self.delta = 1./fps
        self.lastTime = time.time()

    def tick(self):
        t0 = time.time()
        sleepTime = self.lastTime - t0
        if sleepTime > 0:
            time.sleep(sleepTime)
        else:
            print (f"took too long: {sleepTime}")
        self.lastTime = time.time() + self.delta
        




if __name__ == "__main__":
    app = App()
    app.run()
