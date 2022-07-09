from Components.Components import Position
from Components.FlagComponents import IsUI
from Components.PlayerInputComponents import PlayerInput
from Components.UIComponents import CharacterInfoUI
from Controllers import controllers
import json


class EntityManager:
    def __init__(self, level):
        self.level = level
        self.deferred_entities = []

    def update(self):
        self.spawnQueued()

        
    def loadEntities(self, filename):
        with open(filename, 'r') as objectFile:
            objects = json.loads(objectFile.read())
    
        for obj in objects:
            if obj['type'] not in self.level.app.entityDefs.keys():
                self.level.app.entityDefs[obj['type']] = {}
            self.level.app.entityDefs[obj['type']] = obj
    

    def spawn(self, entityType, x = 0, y = 0, inventory = None, parentEntity = None):
        self.deferred_entities.append([entityType, x, y, inventory, parentEntity])

    def spawnQueued(self):
        for e in self.deferred_entities:
            entityType = e[0]
            x = e[1]
            y = e[2]
            inventory = e[3]
            print (f"spawning {entityType}")
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
                self.createUI(entity)

            print ("spawned")
        self.deferred_entities.clear()

    def createUI(self, parentEntity):
        entity = self.level.world.create_entity()
        entity.add(IsUI)
        entity.add(CharacterInfoUI, {'parentEntity': parentEntity})
        entity.add(Position, {
            'x': 0, 
            'y': self.level.height - 8, 
            'width': 22,
            'height': 8,
            'level': self.level})

    def addComponents(self, entity, entityType):
        entityDef = self.level.app.entityDefs[entityType]
        
        if 'inherits' in entityDef.keys():
            self.addComponents(entity, entityDef['inherits'])
        
        for component in entityDef['components'].keys():
            entity.add(component, entityDef['components'][component])
        
