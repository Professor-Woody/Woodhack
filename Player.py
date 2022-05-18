from Entity import Entity
from Actions import CheerAction, MovementAction
import tcod


class Player(Entity):
    def __init__(self, x, y, char, colour, controller):
        super().__init__("PLAYER", char, colour, True)
        self.x = x
        self.y = y
        self.char = char
        self.colour = colour
        self.controller = controller

        self.action1 = CheerAction(self, "Left hand")
        self.action2 = CheerAction(self, "Right hand")


    def performAction(self, action):
        pass

    def update(self, level):
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
            MovementAction(self, dx, dy).perform(level)

        # perform actions based off action keys
        if self.controller.checkKeyPressedOnce(tcod.event.K_z):
            if self.action1:
                self.action1.perform(level)
        elif self.controller.checkKeyPressedOnce(tcod.event.K_x):
            if self.action2:
                self.action2.perform(level)

    def draw(self, screen):
        screen.draw(self.x, self.y, self.char)