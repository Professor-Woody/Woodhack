from ecstremity import World
from Components.Components import Collision, Initiative, Render
from Flags import *
import csv
from Entity import Actor, Entity, EntityDefs


class EntityManager:
    level: World

    def __init__(self, level):
        self.level = level


    def update(self):
        for entity in self.level.create_query(all_of=[Initiative]).result:
            entity.fire_event('tick')

        for entity in self.level.entities:
            entity.fire_event('update')


    def draw(self, screen):
        for entity in self.level.create_query(all_of=[Render]).result:
            entity.draw(screen)


    def add(self, entity):
        self.level.add(entity)


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



    def loadEntities(self, filename):
        with open(filename) as entityDefs:
            reader = csv.reader(entityDefs, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                if row[0] == "NPC":
                    entity = Actor()
                else:
                    entity = Entity()
                    entity.flags.add(OBJECT)

                entity.name = row[1]
                entity.char = row[2]
                entity.fg = (int(row[3]), int(row[4]), int(row[5]))
                if bool(row[6]):
                    entity.collider = CollisionBoxComponent(entity)
                entity.lightRadius = int(row[7])
                if entity.lightRadius:
                    entity.flags.add(LIGHT)

                EntityDefs[entity.name] = entity
    
    def spawn(self, entityName, x, y):
        EntityDefs[entityName].spawn(self.level, x, y)


        
