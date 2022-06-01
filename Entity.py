from Flags import *
from Components.Components import CollisionBoxComponent
from Components.AI import HostileAI
from Actions.EntityActions import MovementAction, GetTargetAction
import Colours as colour
import copy


EntityDefs = {}


class Entity:
    x = 0
    y = 0
    width = 1
    height = 1
    lightRadius = 0
    char='@'
    collider = None
    level = None
    fg=colour.WHITE
    bg=None
    name="Object"

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

    # Target animation variables
    targetCycleSpeed = 0
    targetCycleIndex = 0


    def __init__(self):
        super().__init__()
        self.collider = CollisionBoxComponent(self)
        self.stats = StatsComponent(self)
        self.flags.add(ACTOR)

        self.targettedBy = []

        self.ai = HostileAI(self)

    def update(self):
        super().update()
        # Targetted Animation
        if self.targettedBy:
            self.targetCycleSpeed -= 1
            if self.targetCycleSpeed <= 0:
                self.targetCycleSpeed = 30
                self.targetCycleIndex -= 1
                if self.targetCycleIndex < 0:
                    self.targetCycleIndex = len(self.targettedBy)-1
                self.bg = self.targettedBy[self.targetCycleIndex].fg
        else:
            self.bg = None

        # standard speed check
        if self.speed:
            self.speed -= 1
            return

        self.ai.update()





class Player(Actor):
    lightRadius = 3
    leftHand = None
    rightHand = None

    def __init__(self, controller, fg=colour.WHITE):
        super().__init__()
        self.controller = controller
        self.flags.remove(ACTOR)

        self.flags.add(PLAYER)
        self.flags.add(LIGHT)

        self.fg = fg

        

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
            
        target = None
        if self.controller.getPressedOnce("next"):
            target = "next"
        elif self.controller.getPressedOnce("previous"):
            target = "previous"
        elif self.controller.getPressedOnce("nearestEnemy"):
            target = "nearestEnemy"
        
        if target:
            GetTargetAction(self, target).perform()


    def draw(self, screen):
        screen.draw(self)












class NewPlayer(Player):
    name = "Bob"
    width = 20
    height = 22
    colourIndex = 0
    ready = False

    def __init__(self, controller):
        super().__init__(controller)

    def update(self):
        self.controller.update()
        if not self.ready:
            if self.controller.getPressedOnce("left"):
                self.colourIndex -= 1
                if self.colourIndex < 0:
                    self.colourIndex = len(colour.COLOURS)-1
            if self.controller.getPressedOnce("right"):
                self.colourIndex += 1
                if self.colourIndex >= len(colour.COLOURS):
                    self.colourIndex = 0
            if self.controller.getPressedOnce("use"):
                self.ready = True
            elif self.controller.getPressedOnce("cancel"):
                self.level.unassignedControllers.append(self.controller)
                self.level.entityManager.remove(self)
            self.fg = colour.COLOURS[self.colourIndex]
            
        else:
            if self.controller.getPressedOnce("cancel"):
                self.ready = False
        

    def draw(self, screen):
        if self.ready:
            screen.drawFrame(self.x, self.y, self.width, self.height, title="Ready")

        screen.drawFrame(self.x+1, self.y+1, self.width-2, self.height-2, fg=self.fg)
        screen.printLine(self.x+3, self.y+3, f'"{self.name}"')
        screen.printLine(self.x+3, self.y+5, "Color: ")
        screen.print(self.x+10, self.y+5, self.char, fg=self.fg)

        screen.printLines(self.x+3, self.y+7, "I should\nprobably put\na few lines\nof text to\ndescribe the\nchar here")