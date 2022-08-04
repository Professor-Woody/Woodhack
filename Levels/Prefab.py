from dataclasses import dataclass
from Helpers.LevelCreation import generators
from Levels.Maps import GameMap


@dataclass
class Prefab:
    tiles: list[(int, int), str]
    entryPoints: list[(int, int)]
    connectionType: str = "corridor"
    

    def createRoom(self, tileset: list, gameMap: GameMap):
        pos = gameMap.getPOI()

        for tile in self.tiles:
            coords = (pos[0] + tile[0][0], pos[1] + tile[0][1])
            print (coords)
            gameMap.tiles[coords] = tileset[tile[1]]
            if not gameMap.checkIsPassable(coords[0], coords[1]):
                gameMap.restricted[coords] = True
        
        for point in self.entryPoints:
            coords = (pos[0] + point[0], pos[1] + point[1])
            generators[self.connectionType](coords, gameMap.endSpot, gameMap, tileset['ground'], 10 )