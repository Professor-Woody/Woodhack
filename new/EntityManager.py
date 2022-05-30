from Flags import *

class EntityManager:
    def __init__(self, level):
        self.level = level
        self.entityTypes = set()

        self.allEntities = set()
        self.players = set()
        self.actors = set()
        self.lights = set()
        self.ui = set()


    def update(self):
        for entity in self.allEntities:
            entity.update()

    def draw(self, screen):
        for entity in self.allEntities:
            entity.draw(screen)

    def add(self, entity):
        self.allEntities.add(entity)

        if PLAYER in entity.flags:
            self.players.add(entity)
        if ACTOR in entity.flags:
            self.actors.add(entity)
        if LIGHT in entity.flags:
            self.lights.add(entity)
        if UI in entity.flags:
            self.ui.add(entity)


    def remove(self, entity):
        self.allEntities.remove(entity)

        if entity in self.players:
            self.players.remove(entity)
        if entity in self.actors:
            self.actors.remove(entity)
        if entity in self.lights:
            self.lights.remove(entity)
        if entity in self.ui:
            self.ui.remove(entity)

    def checkIsBlocked(self, x, y):
        for entity in self.allEntities:
            if entity.collider and entity.collider.pointCollides(x, y):
                return entity



        
