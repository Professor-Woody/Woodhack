from dataclasses import dataclass
from Components.Components import Collision, Initiative, Light, Player, Position, Render, Stats
from Flags import *
import csv

@dataclass
class Test:
    screen: any

class EntityManager:
    def __init__(self, level):
        self.level = level


    def update(self):
        for entity in self.level.world.create_query(all_of=[Initiative]).result:
            entity.fire_event('tick')

        for entity in self.level.world.entities:
            entity.fire_event('update')


    def draw(self, screen):
        for entity in self.level.world.create_query(all_of=[Render]).result:            
            entity.fire_event('draw', {"screen": screen})
            # entity[Render].on_draw(Test(screen))


    def add(self, entity):
        self.level.world.add(entity)


    def remove(self, entity):
        self.level.world.remove(entity)



    def loadEntities(self, filename):
        with open(filename) as entityDefs:
            reader = csv.reader(entityDefs, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                self.level.app.entityDefs[row[1]] = row.copy()


    
    def spawn(self, entityName, x, y):
        row = self.level.app.entityDefs[entityName]
        entity = self.level.world.create_entity()
        
        entity.add(Position, {"x": x, "y": y})
        entity.add(Render, {
            "map": self.level.map,
            "entityName": row[1],
            "char": row[2],
            "fg": (int(row[3]), int(row[4]), int(row[5]))
            })

        row[7] = 3
        if int(row[7]):
            entity.add(Light, {"radius": int(row[7])})
        
        if row[0] == "NPC":
            entity.add(Collision)
            entity.add(Initiative)
            entity.add(Stats, {"hp": 10})
            entity.add(Player)


        
