from random import randint, choice
import Helpers.PositionHelper as PositionHelper


HULKS = 80
HULKSTEPS = 100
DIR = [-1, 1]

def createCaverns(gameMap, tileset):
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

