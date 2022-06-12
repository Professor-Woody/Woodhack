from cmath import e
from dataclasses import dataclass
from Components.Components import BlocksMovement, Inventory, IsItem, IsNPC, Collision, Initiative, Light, IsPlayer, PlayerInput, Position, Render, Stats, Target, Targeted, UIPosition, LeftHand, RightHand
from Controllers import controllers
import csv



@dataclass
class Test:
    screen: any

class EntityManager:
    def __init__(self, level):
        self.level = level
        self.deferred_entities = []

    def update(self):
        for entity in self.level.world.create_query(all_of=[Initiative]).result:
            entity.fire_event('tick')
            # entity[Initiative].on_tick(None)
        
        actions = []
        for entity in self.level.world.entities:
            actions += entity.fire_event('update', {'actions': []}).data.actions

        for action in actions:
            action.perform()

        for entity in self.deferred_entities:
            self.add(entity)
        self.deferred_entities = []

    def draw(self, screen):
        for entity in self.level.world.create_query(all_of=[Render]).result:            
            entity.fire_event('draw', {"screen": screen})
            # entity[Render].on_draw(Test(screen))

    def addEntity(self, entity):
        print (f"adding {entity}")
        self.deferred_entities.append(entity)

    def add(self, entity):
        self.level.world.add(entity)
        entity[Position].level = self.level



    def remove(self, entity):
        self.level.world.remove(entity)
        entity[Position].level = None



    def loadEntities(self, filename):
        with open(filename) as entityDefs:
            reader = csv.reader(entityDefs, delimiter=',', quotechar='"')
            next(reader, None)
            for row in reader:
                self.level.app.entityDefs[row[1]] = row.copy()


    
    def spawn(self, entityName, x, y):
        row = self.level.app.entityDefs[entityName]
        entity = self.level.world.create_entity()
        
        entity.add(Position, {"x": x, "y": y, "level": self.level})
        entity.add(Render, {
            "map": self.level.map,
            "entityName": row[1],
            "char": row[2],
            "fg": (int(row[3]), int(row[4]), int(row[5]))
            })

        if int(row[7]):
            entity.add(Light, {"radius": int(row[7])})
        
        if row[0] == "OBJECT":
            entity.add(IsItem)
            entity.add(Collision)

        if row[0] == "NPC" or row[0] == "PLAYER":
            entity.add(Collision)
            entity.add(BlocksMovement)
            entity.add(Initiative)
            entity.add(Target)
            entity.add(Stats, {"hp": 10, "moveSpeed": int(row[8])})

        if row[0] == "NPC":
            entity.add(IsNPC)
            entity.add(Targeted)

        if row[0] == "PLAYER":
            entity.add(IsPlayer)
            entity.add(PlayerInput, {"controller": controllers[0]})
            entity.add(LeftHand)
            entity.add(RightHand)
            entity.add(UIPosition, {
                'sideX': self.level.width - 30,
                'sideY': self.level.sideY,
                'bottomX': self.level.bottomX,
                'bottomY': self.level.height - 10
                })
            entity.add(Inventory)
            self.level.sideY += 14
            self.level.bottomX += 16



        
