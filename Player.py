from Entity import Entity
from Actions import CheerAction, MovementAction
import tcod


class Player(Entity):
    def __init__(self, x, y, char, colour, controller, level):
        super().__init__("PLAYER", char, colour, True)
        self.x = x
        self.y = y
        self.controller = controller
        self.level = level

        self.action1 = CheerAction(self, "Left hand")
        self.action2 = CheerAction(self, "Right hand")


    def performAction(self, action):
        pass

    def update(self):
        # check movement
        dx = 0
        dy = 0
        if self.controller.checkKeyPressedOnce(tcod.event.K_UP):
            dy -= 1
        if self.controller.checkKeyPressedOnce(tcod.event.K_DOWN):
            dy += 1
        if self.controller.checkKeyPressedOnce(tcod.event.K_LEFT):
            dx -= 1
        if self.controller.checkKeyPressedOnce(tcod.event.K_RIGHT):
            dx += 1

        if dx or dy:
            print (dx, dy)
            MovementAction(self, dx, dy).perform()

        # perform actions based off action keys
        if self.controller.checkKeyPressedOnce(tcod.event.K_z):
            if self.action1:
                self.action1.perform()
        elif self.controller.checkKeyPressedOnce(tcod.event.K_x):
            if self.action2:
                self.action2.perform()

    def draw(self, screen):
        screen.draw(self.x, self.y, self.char)