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
            self.level.app.entityDefs[obj['type']] = obj
    

    def spawn(self, entityType, x = 0, y = 0, inventory = None):
        entity = self.level.world.create_entity()
        self.addComponents(entity, entityType)

        if not inventory:
            entity.add(Position, {
                'level': self.level,
                'x': x,
                'y': y
            })
        else:
            inventory.inventory.add(entity)

        if entityType == "PLAYER":
            entity.add(PlayerInput, {'controller': controllers[0]})




    def addComponents(self, entity, entityType):
        entityDef = self.level.app.entityDefs[entityType]
        
        if 'inherits' in entityDef.keys():
            self.addComponents(entity, entityDef['inherits'])
        
        for component in entityDef['components'].keys():
            entity.add(component, entityDef['components'][component])
        
