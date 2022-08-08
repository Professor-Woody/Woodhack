from random import choice, randint
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
        biomeType = biomeDef['type']

        self.mapGenerator = biomeDef['mapGenerator']
        self.tileset = self.createTileset(biomeDef['tileset'])
        self.requiredPrefabs = [Prefab(prefab) for prefab in biomeDef['requiredPrefabs']] if 'requiredPrefabs' in biomeDef.keys() else {}
        self.optionalPrefabs = [Prefab(prefab) for prefab in biomeDef['optionalPrefabs']] if 'optionalPrefabs' in biomeDef.keys() else {}
        self.optionalMin = biomeDef['optionalMin']  if 'optionalMin' in biomeDef.keys() else 0
        self.optionalMin = biomeDef['optionalMin']  if 'optionalMax' in biomeDef.keys() else 0
        

    def createLevel(self, level, gameMap):
        self.createBaseMap(level, gameMap)
        self.createRequiredPrefabs(level, gameMap)
        self.createOptionalPrefabs(level, gameMap)
        self.createStartPoint(level, gameMap)
        self.createExitPoint(level, gameMap)

        # TODO: create additional spawners for random monsters


    # ------------------------------------------
    def createTileset(self, tileset):
        for tile in tileset.keys():
            if tile[-1] == 's':
                # it's plural, so there's multiple tiles inside here
                self.createTileset(tile)
            else:
                self.tileset[tile] = newTile(
                                        tileset[tile]['passable'],
                                        tileset[tile]['transparent'],
                                        tileset[tile]['dark'],
                                        tileset[tile]['light'])


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
        Generators[self.mapGenerator](level, gameMap)



    # ------------------------------------------
    def createStartPoint(self, level, gameMap):
        # if the level already contains an entry point, put ours there

        level.startPoint = choice(level.POIs) if not level.startPoint else level.startPoint

        drawShape((level.startPoint[0], level.startPoint[1]), 'square2', self.tileset['floor'], gameMap)
        level.e.spawn('stairsUp', level.startPoint[0], level.startPoint[1])



    # ------------------------------------------
    def createExitPoint(self, level, gameMap):
        level.exitPoint = level.getPOI() if not level.exitPoint else level.exitPoint

        drawShape((level.exitPoint[0], level.exitPoint[1]), 'square2', self.tileset['floor'], gameMap)
        level.e.spawn('stairsDown', level.exitPoint[0], level.exitPoint[1])
        Generators['smallTunnel']((level.start[0], level.start[1]), (level.exitPoint[0], level.exitPoint[1]))
    
        
