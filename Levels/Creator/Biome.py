from random import choice, choices, randint
from EntityManager import Entity
from Levels.Creator.Generators import Generators
from Levels.Creator.Prefabs import Prefab
from Levels.Creator.Shapes import drawShape
from Levels.Creator.Tiles import newTile


class Biome:
    mapGenerator: str
    tileset: dict
    requiredPrefabs: list
    optionalPrefabs: list
    optionalMin: int
    optionalMax: int
    randomStartPoint: bool = True

    def __init__(self, biomeDef) -> None:
        self.type = biomeDef['type']

        self.mapGenerator = biomeDef['mapGenerator']
        self.tileset = {}
        self.tilesetWeights = {}
        self.createTileset(biomeDef['tileset'])
        self.requiredPrefabs = [Prefab(prefab) for prefab in biomeDef['requiredPrefabs']] if 'requiredPrefabs' in biomeDef.keys() else {}
        self.optionalPrefabs = [Prefab(prefab) for prefab in biomeDef['optionalPrefabs']] if 'optionalPrefabs' in biomeDef.keys() else {}
        self.optionalMin = biomeDef['optionalMin']  if 'optionalMin' in biomeDef.keys() else 0
        self.optionalMin = biomeDef['optionalMin']  if 'optionalMax' in biomeDef.keys() else 0
        

    def createLevel(self, level, gameMap):
        self.createBaseMap(level, gameMap)
        self.createRequiredPrefabs(level, gameMap)
        #self.createOptionalPrefabs(level, gameMap)
        self.createStartPoint(level, gameMap)
        self.createExitPoint(level, gameMap)

        # TODO: create additional spawners for random monsters


    # ------------------------------------------t
    def createTileset(self, tileset): 
        for tile in tileset:
            tile['tile']['dark'][0] = ord(tile['tile']['dark'][0])
            tile['tile']['light'][0] = ord(tile['tile']['light'][0])
            
            if tile['type'] not in self.tileset.keys():
                self.tileset[tile['type']] = []
                self.tilesetWeights[tile['type']] = []

            nt = newTile(
                    tile['type'],
                    tile['tile']['passable'],
                    tile['tile']['transparent'],
                    tuple(tile['tile']['dark']),
                    tuple(tile['tile']['light']))
            self.tileset[tile['type']].append(nt)

            self.tilesetWeights[tile['type']].append(tile['weight'] if 'weight' in tile.keys() else 100)

    # ------------------------------------------
    def createRequiredPrefabs(self, level, gameMap):
        for prefab in self.requiredPrefabs:
            prefab.create(level, gameMap, self.tileset)

    


    # ------------------------------------------
    def createOptionalPrefabs(self, level, gameMap):
        extraRooms = randint(self.optionalMin, self.optionalMax)
        usedRooms = set()
        for i in range(extraRooms):
            room = choice(self.optionalPrefabs)
            if room not in usedRooms or room.allowMultiple:
                room.create(level, gameMap, self.tileset)
                usedRooms.set(room)
        


    # ------------------------------------------
    def createBaseMap(self, level, gameMap):
        for x in range(gameMap.width):
            for y in range(gameMap.height):
                gameMap.tiles[x,y] = self.getTile('wall')
        Generators[self.mapGenerator](level, self, gameMap)



    # ------------------------------------------
    def createStartPoint(self, level, gameMap):
        # if the level already contains an entry point, put ours there

        gameMap.startPoint = gameMap.getPOI() if not gameMap.startPoint else gameMap.startPoint
        print ("=======================")
        print (f"Start point: {gameMap.startPoint}")
        drawShape((gameMap.startPoint[0], gameMap.startPoint[1]), 'square2', self, 'floor', gameMap)
        level.e.spawn('StairsUp', gameMap.startPoint[0], gameMap.startPoint[1])



    # ------------------------------------------
    def createExitPoint(self, level, gameMap):
        gameMap.exitPoint = gameMap.getPOI() if not gameMap.exitPoint else gameMap.exitPoint
        drawShape((gameMap.exitPoint[0], gameMap.exitPoint[1]), 'square2', self, 'floor', gameMap)
        level.e.spawn('StairsDown', gameMap.exitPoint[0], gameMap.exitPoint[1])
        Generators['corridor'](
            (gameMap.startPoint[0], gameMap.startPoint[1]), 
            (gameMap.exitPoint[0], gameMap.exitPoint[1]),
            self,
            gameMap)
    
        
    def getTile(self, tileType):
        result = choices(self.tileset[tileType], self.tilesetWeights[tileType])[0]
        return result
