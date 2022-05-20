from Entity import Entity
from Actions import CheerAction, MovementAction
import tcod
import UI as ui


class Player(Entity):
    def __init__(self, x, y, char, colour, controller, level):
        super().__init__("PLAYER", char, colour, True)
        self.x = x
        self.y = y
        self.controller = controller
        self.level = level

        self.action1 = CheerAction(self, "Left hand")
        self.action2 = CheerAction(self, "Right hand")

        self.speed = 0
        self.hp = 5
        self.maxHP = 5


    def performAction(self, action):
        pass

    def update(self):
        if self.speed:
            self.speed -= 1
            return
        
        # check movement
        dx = 0
        dy = 0
        if self.controller.checkKeyPressed(tcod.event.K_UP):
            dy -= 1
        if self.controller.checkKeyPressed(tcod.event.K_DOWN):
            dy += 1
        if self.controller.checkKeyPressed(tcod.event.K_LEFT):
            dx -= 1
        if self.controller.checkKeyPressed(tcod.event.K_RIGHT):
            dx += 1

        if dx or dy:
            WaitAction(self, 30).perform()
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
        ui.renderHPBar(screen, self.hp, self.maxHP, 20)