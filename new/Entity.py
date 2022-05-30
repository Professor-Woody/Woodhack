from Flags import *
from Components import CollisionBoxComponent
from EntityActions import MovementAction
import Colours as colour
import copy


class Entity:
    x = 0
    y = 0
    width = 1
    height = 1
    lightRadius = 0
    char='@'
    collider = None
    level = None

    def __init__(self):
        self.flags = set()

    def place(self, level, x, y):
        self.x = x
        self.y = y
        if self.level:
            self.level.entityManager.remove(self)
        self.level = level
        self.level.entityManager.add(self)


    def spawn(self, level, x, y):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.level = level
        level.entityManager.add(clone)

    def despawn(self):
        self.level.entityManager.remove(self)

    def update(self):
        pass

    def draw(self, screen):
        if self.level.map.checkIsVisible(self):
            screen.draw(self)

    def move(self, x, y):
        self.x = x
        self.y = y



class Actor(Entity):
    speed = 0
    target = None

    def __init__(self):
        super().__init__()
        self.collider = CollisionBoxComponent(self)
        self.flags.add(ACTOR)

    def update(self):
        super().update()
        if self.speed:
            self.speed -= 1
            return




class Player(Actor):
    lightRadius = 3
    leftHand = None
    rightHand = None

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.flags.remove(ACTOR)

        self.flags.add(PLAYER)
        self.flags.add(LIGHT)

        

    def update(self):
        if self.speed:
            self.speed -= 1
            return
        
        self.controller.update()

        # Movement
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

        # use equipped items
        if self.leftHand and self.controller.getPressed("leftHand"):
            self.leftHand.use()
        elif self.rightHand and self.controller.getPressed("rightHand"):
            self.rightHand.use()
            

    def draw(self, screen):
        screen.draw(self)


class NewPlayer(Player):
    name = "Bob"
    width = 18
    height = 30
    colourIndex = 0
    ready = False

    def __init__(self, controller):
        super().__init__(controller)
        print (self.flags)

    def update(self):
        self.controller.update()
        if self.controller.getPressedOnce("left"):
            print (self.controller.checked)
            self.colourIndex -= 1
            if self.colourIndex < 0:
                self.colourIndex = len(colour.COLOURS)-1
        if self.controller.getPressedOnce("right"):
            self.colourIndex += 1
            if self.colourIndex >= len(colour.COLOURS):
                self.colourIndex = 0
        if self.controller.getPressedOnce("up"):
            self.ready = True
        
        if self.controller.getPressedOnce("cancel"):
            self.level.unassignedControllers.add(self.controller)
            self.level.entityManager.remove(self)
        

    def draw(self, screen):
        if self.ready:
            screen.drawFrame(self.x, self.y, self.width, self.height, fg=colour.COLOURS[self.colourIndex])
        else:
            screen.drawFrame(self.x, self.y, self.width, self.height)
        screen.printLine(self.x+4, self.y+2, self.name)
        screen.printLine(self.x+4, self.y+3, "Color: ")
        screen.print(self.x+11, self.y+3, self.char, fg=colour.COLOURS[self.colourIndex])

        screen.printLines(self.x+4, self.y+5, "I should\nprobably put\na few lines\nof text to\ndescribe the\nchar here")