from random import randint
import Helpers.PositionHelper as PositionHelper


class Prefab:
    def __init__(self, prefabDef):
        self.tiles = prefabDef['tiles']
        self.connectPoints = prefabDef['connectPoints'] if 'connectPoints' in prefabDef.keys() else []
        self.entities = prefabDef['entities'] if 'entities' in prefabDef.keys() else []

    def create(self, level, gameMap, tileset):
        # alter the gamemap
        pos = level.getPOI()


        for tile in self.tiles:
            loc = pos[0] + tile['pos'][0], pos[1] + tile['pos'][1]
            gameMap.tiles[loc] = tileset[tile['type']]



        # create a connecting path if needed
        for point in self.connectPoints:
            loc = pos[0] + point[0], pos[1] + point[1]
            path = PositionHelper.getPathTo(loc, level.POIs[0], gameMap, 20)



        # spawn entities
        for entity in self.entities:
            level.e.spawn(entity['type'], entity['pos'][0], entity['pos'][1])