import json
from Levels.Creator.Prefabs import Prefab
from Levels.Maps import GameMap
from Levels.Creator.Biome import Biome


class NewLevelCreator:
    biomes = {}
    prefabs = {}

    @classmethod    
    def loadTemplates(cls):
        with open('biomes.json', 'r') as objectFile:
            objects = json.loads(objectFile.read())
        
        for obj in objects:
            biome = Biome(obj)
            cls.biomes[biome.type] = biome

    @classmethod
    def createLevel(cls, level, biomeType):
        gameMap = GameMap(level, level.width, level.height)
        biome = cls.biomes[biomeType]
        biome.createLevel(level, gameMap)

