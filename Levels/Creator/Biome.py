from random import choice, randint
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
        for tile in tileset.keys():
            if tile[-1] == 's':
                # it's plural, so there's multiple tiles inside here
                self.createTileset(tileset[tile])
            else:

                tileset[tile]['dark'][0] = ord(tileset[tile]['dark'][0])
                tileset[tile]['light'][0] = ord(tileset[tile]['light'][0])
                self.tileset[tile] = newTile(
                                        tileset[tile]['passable'],
                                        tileset[tile]['transparent'],
                                        tuple(tileset[tile]['dark']),
                                        tuple(tileset[tile]['light']))


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
        Generators[self.mapGenerator](level, gameMap, self.tileset)



    # ------------------------------------------
    def createStartPoint(self, level, gameMap):
        # if the level already contains an entry point, put ours there

        gameMap.startPoint = gameMap.getPOI() if not gameMap.startPoint else gameMap.startPoint
        print ("=======================")
        print (f"Start point: {gameMap.startPoint}")
        drawShape((gameMap.startPoint[0], gameMap.startPoint[1]), 'square2', self.tileset['floor'], gameMap)
        level.e.spawn('StairsUp', gameMap.startPoint[0], gameMap.startPoint[1])



    # ------------------------------------------
    def createExitPoint(self, level, gameMap):
        gameMap.exitPoint = gameMap.getPOI() if not gameMap.exitPoint else gameMap.exitPoint
        drawShape((gameMap.exitPoint[0], gameMap.exitPoint[1]), 'square2', self.tileset['floor'], gameMap)
        level.e.spawn('StairsDown', gameMap.exitPoint[0], gameMap.exitPoint[1])
        Generators['corridor'](
            (gameMap.startPoint[0], gameMap.startPoint[1]), 
            (gameMap.exitPoint[0], gameMap.exitPoint[1]),
            gameMap,
            self.tileset)
    
        
