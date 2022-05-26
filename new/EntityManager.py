from Flags import *

class EntityManager:
    entityTypes = set()

    allEntities = set()
    players = set()
    actors = set()
    lights = set()
    ui = set()

    def __init__(self, level):
        self.level = level

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



        
