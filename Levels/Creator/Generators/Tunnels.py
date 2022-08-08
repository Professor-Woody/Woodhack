from random import choice
import Helpers.PositionHelper as PositionHelper
from Levels.Creator.Shapes import *

def createTunnel(start, end, gameMap, tile):
    # get the path with getLOS


    # split the path up into 3-8 segments

    # randomly move the segment

    # blot the segments with larger caverns

    # get the new LOS between each segment

    # build 3 wide tunnel between each segment

    path = PositionHelper.getPathTo(start, end, gameMap, True)
    for (x,y) in path:
        gameMap.tiles[x, y] = tile
        for s in shapes[choice(['diamond2', 'diamond3', 'square2', 'square2', 'square2', 'square3', 'circle3'])]:
            gameMap.tiles[x + s[0], y + s[1]] = tile




def createCorridor(start, end, gameMap, tile, goThroughWalls = 3):
        path = PositionHelper.getPathTo(start, end, gameMap, goThroughWalls, 0, True)
        for (x, y) in path:
            gameMap.tiles[x, y] = tile
            gameMap.tiles[x,y]['light']['fg'] = (255, 0, 0)




def createSmallTunnel(start, end, gameMap, tile):
    pass



def createSmallCorridor(start, end, gameMap, tile):
    pass