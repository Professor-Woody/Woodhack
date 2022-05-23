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

        self.speed = 0

        self.action1 = CheerAction(self, "Left hand")
        self.action2 = CheerAction(self, "Right hand")

        self.speed = 0
        self.hp = 5
        self.maxHP = 5

        self.lightRadius = 5

        self.ui = ui.TextBox(1, 40, "testing\nsome\nstuff", "Woody")


    def update(self):

        if self.speed > 0:
            self.speed -= 1
            return

        # check movement
        dx = 0
        dy = 0
        if self.controller.getPressed("up"):
            dy -= 1
        if self.controller.getPressed("down"):
            dy += 1
        if self.controller.getPressed("left"):
            dx -= 1
        if self.controller.getPressed("right"):
            dx += 1

        if dx or dy:
            MovementAction(self, dx, dy, 6).perform()

        # perform actions based off action keys
        if self.controller.getPressed("lefthand"):
            if self.action1:
                self.action1.perform()
        elif self.controller.getPressed("righthand"):
            if self.action2:
                self.action2.perform()
        self.ui.update()
        

    def draw(self, screen):
        screen.draw(self)
        self.ui.draw(screen)
        #screen.drawFrame(0, 40, "test", "testing\nsome stuff")
        #ui.renderHPBar(screen, 0, 45, self.hp, self.maxHP, 20)