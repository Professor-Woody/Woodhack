import Helpers.PositionHelper as PositionHelper
from random import randint, choice
import numpy as np
from random import randint, choice
from EntityManager import add_bit

graphic_dt = np.dtype(
    [
        ("ch", np.int32),
        ("fg", "3B"),
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("passable", np.bool),
        ("transparent", np.bool),
        ("dark", graphic_dt),
        ("light", graphic_dt)
    ]
)

SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

def newTile(passable, transparent, dark, light):
    return np.array((passable, transparent, dark, light), dtype=tile_dt)

# TILES
floor = newTile(
    passable=True, 
    transparent=True,
    dark=(ord(" "), (100,100,100), (10, 10, 10)),
    light=(ord(" "), (200, 200, 200), (100, 100, 100)),
)

ground = newTile(
    passable=True, 
    transparent=True,
    dark=(ord("."), (100,100,100), (10, 10, 10)),
    light=(ord("."), (200, 200, 200), (100, 100, 100)),
)

wall = newTile(
    passable=False, 
    transparent=False, 
    dark=(ord("#"), (100,100,100), (10, 10, 10)),
    light=(ord("#"), (200, 200, 200), (100, 100, 100)),
)

wall2 = newTile(
    passable=False, 
    transparent=False, 
    dark=(ord("█"), (100,100,100), (10, 10, 10)),
    light=(ord("█"), (200, 200, 200), (100, 100, 100)),
)

HULKS = 80
HULKSTEPS = 100
DIR = [-1, 1]


surrounding = [
    (-1,-1), (0,-1), (1, -1),
    (-1,0), (1,0),
    (-1,1), (0,1), (1,1)
    ]


square2 = [(x-1,y-1) for x in range(3) for y in range(3)] 
square2.pop(4)
square3 = [(x-2,y-2) for x in range(5) for y in range(5)] 
square3.pop(12)
diamond2 = [(0,-1),(-1, 0), (1, 0),(0, 1)]
diamond3 = [(0, -2),(-1, -1), (0, -1), (1, -1),(-2, 0), (-1, 0), (1, 0), (2, 0),(-1, 1), (0, 1), (1, 1),(0, 2)]
circle3 = [(-1, -2), (0, -2), (1, -2),(-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),(-2, 0), (-1, 0), (1, 0), (2, 0),(-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),(-1, 2), (0, 2), (1, 2),]

shapes = {
    'square2': square2,
    'square3': square3,
    'diamond2': diamond2,
    'diamond3': diamond3,
    'circle3': circle3
}


def createCaverns(gameMap):
    # drunken umber hulk approach
    # randomly stagger around the map digging out areas
    # make the first and last place the start and end points

    pointsOfInterest = []
    print ("creating caverns")

    for hulk in range(HULKS):
        x = randint(5, gameMap.width - 5)
        y = randint(5, gameMap.height - 5)
        pointsOfInterest.append((x,y))
        

        for step in range(HULKSTEPS):
            dx = 0
            dy = 0
            if randint(0,1):
                dx = choice(DIR)
            else:
                dy = choice(DIR)
            x += dx
            y += dy
            if x < 2 or x > gameMap.width - 2:
                x -= dx
            if y < 2 or y > gameMap.height - 2:
                y -= dy
            
            gameMap.tiles[x, y] = ground

    # Ensure every part of the map is reachable
    for i in range(len(pointsOfInterest) - 1):
        path = PositionHelper.getPathTo(pointsOfInterest[i], pointsOfInterest[i+1], gameMap)
        if not len(path):
            createTunnel(pointsOfInterest[i], pointsOfInterest[i+1], gameMap, ground)

    # trim away the majority of stragglers/orphaned walls
    clearList = [0, 1, 2, 4, 8, 16, 32, 64, 128]
    for y in range(1, gameMap.height - 2):
        for x in range(1, gameMap.width - 2):
            if gameMap.tiles[x, y]['light']['ch'] == ord('#'):
                value = getTileShapeValue((x,y), gameMap)
                if value in clearList:
                    gameMap.tiles[x, y] = ground

    # restore the border walls
    gameMap.tiles[0:gameMap.width-1, 0] = wall
    gameMap.tiles[0, 0:gameMap.height-1] = wall
    gameMap.tiles[0:gameMap.width-1, gameMap.height-1] = wall
    gameMap.tiles[gameMap.width-1, 0:gameMap.height-1] = wall

    gameMap.pointsOfInterest = pointsOfInterest



def getTileShapeValue(pos, gameMap):
    value = 0
    counter = 0
        
    for s in surrounding:
        tile = gameMap.tiles[pos[0]+s[0], pos[1]+s[1]]
        # print (tile['light']['ch'])
        if tile['light']['ch'] == ord('#'):
            value = add_bit(value, counter)
        counter += 1
    return value
    

def createDungeon(gameMap):
    pass

def createCaves(gameMap):
    pass

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

generators = {
    "caverns": createCaverns,
    "dungeon": createDungeon,
    "caves": createCaves,
    "tunnel": createTunnel,
    "corridor": createCorridor,
    "smallTunnel": createSmallTunnel,
    "smallCorridor": createSmallCorridor
}

def drawShape(pos, shape, tile, gameMap):
    for (dx,dy) in shapes[shape]:
        x = pos[0] + dx
        y = pos[1] + dy
        gameMap.tiles[x,y] = tile
