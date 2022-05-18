import csv
import copy

class Entity:
    x = 0
    y = 0
    level = None

    def __init__(self, eType, char, colour, blocksMovement=False):
        self.char = char
        self.colour = colour
        self.type = eType
        self.blocksMovement = blocksMovement

    def draw(self, screen, gameMap):
        if gameMap.visible[self.x, self.y]:
            screen.draw(self.x, self.y, self.char)

    def update(self, level):
        pass

    def move(self, x, y):
        self.x = x
        self.y = y

    def place(self, level, x, y):
        self.x = x
        self.y = y
        if self.level:
            self.level.entityManager.remove(self)
        self.level = level
        self.level.entityManager.add(self)
    
    def spawn(self, entityManager, x, y):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y

        entityManager.add(clone)


class NPC(Entity):
    def __init__(self, breed, ai=BaseAI(self)):
        self.breed = breed
        self.ai = ai

    def update(self, level):
        pass

    