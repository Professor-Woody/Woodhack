from Components import CollisionBoxComponent
from Entity import Entity
import Colours as colour
from Flags import *

class UIEntity(Entity):
    def mouseMotion(self, x, y):
        pass

    def mouseClick(self, button, x, y):
        pass


class Text(UIEntity):
    def __init__(self, msg, ttl = -1, needsVisibility=False):
        super().__init__()
        self.msg = msg
        self.ttl = ttl
        self.needsVisibility = needsVisibility
        self.flags.add(UI)

    def update(self):
        if self.ttl != -1:
            self.ttl -= 1
            if self.ttl == 0:
                self.despawn()

    def draw(self, screen):
        if not self.needsVisibility or (self.needsVisibility and self.level.map.checkIsVisible(self)):
            screen.printLine(self.x, self.y, self.msg)



class Button(UIEntity):
    selected = False

    def __init__(self, msg, action=None, width=0, height=0):
        super().__init__()
        self.collider = CollisionBoxComponent(self)
        self.width = width
        self.height = height
        self.msg = msg
        self.flags.add(UI)

        if not width:
            lines = msg.split("\n")
            length = 0
            for line in lines:
                if len(line) > length:
                    length = len(line)
            self.width = length + 4
            self.height = len(lines) + 4

        self.action = action

        self.deselect()
        
    def mouseMotion(self, x, y):
        if self.collider.pointCollides(x, y):
            self.select()
        else:
            self.deselect()

    def select(self):
        self.bg = colour.LIGHT_GREY
        self.fg = colour.BLACK

    def deselect(self):
            self.bg = colour.GREY
            self.fg = colour.WHITE

    def mouseClick(self, button, x, y):
        if self.collider.pointCollides(x, y):
            if self.action:
                self.action.perform()

    def draw(self, screen):
        screen.drawFrame(self.x, self.y, self.width, self.height, bg=self.bg, fg=self.fg)
        if self.msg.count("\n"):
            screen.printLines(self.x+2, self.y+2, self.msg, self.fg, self.bg)
        else:
            screen.printLine(self.x+2, self.y+2, self.msg, self.fg, self.bg)
