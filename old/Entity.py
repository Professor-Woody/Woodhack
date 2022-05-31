import copy
from Components import BaseAI, Breed, HostileAI

class Entity:
    x = 0
    y = 0
    lightRadius = 0
    level = None

    def __init__(self, eType, char, colour, blocksMovement=False, lightRadius=0):
        self.char = char
        self.colour = colour
        self.type = eType
        self.blocksMovement = blocksMovement
        self.lightRadius=lightRadius

    def draw(self, screen):
        if self.level.map.checkIsVisible(self):
            screen.draw(self)

    def update(self):
        pass

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

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


class Actor(Entity):
    def __init__(self, eType, char, colour, blocksMovement=False, breed=None, ai=None):
        super().__init__(eType, char, colour, blocksMovement)

        # components
        if not breed:
            breed=Breed(8,1)
        self.breed = breed
        if not ai:
            ai = HostileAI(self)
        self.ai = ai

        self.speed = 0
        self.target = None


    def update(self):
        if self.speed:
            self.speed -= 1
            return
        self.ai.perform()

    
