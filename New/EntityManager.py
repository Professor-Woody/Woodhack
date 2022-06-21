from Components.Components import PlayerInput, Position
from Controllers import controllers
import json


class EntityManager:
    def __init__(self, level):
        self.level = level
        self.deferred_entities = []


    def loadEntities(self, filename):
        with open(filename, 'r') as objectFile:
            objects = json.loads(objectFile.read())
    
        for obj in objects:
            if obj['type'] not in self.level.app.entityDefs.keys():
                self.level.app.entityDefs[obj['type']] = {}
            self.level.app.entityDefs[obj['type']][obj['name']] = obj
    

    def spawn(self, entityType, entityName, x, y):
        entityDef = self.level.app.entityDefs[entityType][entityName]
        entity = self.level.world.create_entity()
        for component in entityDef['components'].keys():
            entity.add(component, entityDef['components'][component])
        
        entity[Position].level = self.level
        entity[Position].x = x
        entity[Position].y = y

        if entityType == "PLAYER":
            entity.add(PlayerInput, {'controller': controllers[0]})
