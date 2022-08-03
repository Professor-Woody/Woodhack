from dataclasses import dataclass
from Helpers.LevelCreation import generators
from Levels.Maps import GameMap


@dataclass
class Prefab:
    tiles: dict[str: ((int, int), str)]
    entryPoints: list[(int, int)]
    connectionType: str = "tunnel"
    

    def createRoom(self, tileset: list, gameMap: GameMap):
        for tile in self.tiles:
            gameMap.tiles[tile[0]] = tileset[tile[1]]
            gameMap.restricted[tile[0]] = True
        
        for point in self.entryPoints:
            generators[self.connectionType](point, gameMap.endSpot, gameMap, tileset['ground'] )