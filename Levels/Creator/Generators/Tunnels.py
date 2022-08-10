from random import choice
import Helpers.PositionHelper as PositionHelper
from Levels.Creator.Shapes import *
import time


def createTunnel(start, end, biome, gameMap):

    path = PositionHelper.getPathTo(start, end, gameMap, True)
    for (x,y) in path:
        gameMap.tiles[x, y] = biome.getTile('floor')
        for s in shapes[choice(['diamond2', 'diamond3', 'square', 'square', 'square2', 'square', 'square', 'square'])]:
            gameMap.tiles[x + s[0], y + s[1]] = biome.getTile('floor')
            # #tempdraw
            # gameMap.level.app.screen.drawArray((0,gameMap.width), (0, gameMap.height), gameMap.tiles['light'])
            # gameMap.level.app.screen.flip()


def createCorridor(start, end, biome, gameMap, goThroughWalls = 3):
        path = PositionHelper.getPathTo(start, end, gameMap, goThroughWalls, 0, True)
        for (x, y) in path:
            gameMap.tiles[x, y] = biome.getTile('floor')
            gameMap.tiles[x, y]['light']['fg'] = (255, 0, 0)
            # time.sleep(.01)




def createSmallTunnel(start, end, gameMap, tile):
    pass



def createSmallCorridor(start, end, gameMap, tile):
    pass