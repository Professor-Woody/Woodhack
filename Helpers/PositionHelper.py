import tcod
import numpy as np

def getRange(entityCoords, otherCoords):
    return max(abs(entityCoords[0] - otherCoords[0]), abs(entityCoords[1] - otherCoords[1]))


def getLOS(entityCoords, otherCoords, visionRange, Map):
    path = tcod.los.bresenham(
        (entityCoords[0], entityCoords[1]),
        (otherCoords[0], otherCoords[1])
    ).tolist()
    if len(path)-1 > visionRange:
        return False

    for x, y in path[1:-1]:
        if not Map.checkIsPassable(x,y) \
            or Map.checkIsBlocked(x, y):
            return False
    return path    


def getAngleLine(entityCoords, otherCoords, length=100, Map=None):
    path = tcod.los.bresenham(
        (entityCoords[0], entityCoords[1]),
        (otherCoords[0], otherCoords[1])
    ).tolist()

    path = path[:length]
    if Map:
        counter = 1
        for x, y in path[:-1]:
            if (Map.checkIsPassable(x, y) or Map.checkIsBlocked(x, y)):
                path = path[1: counter]
                break
            counter += 1
        
    return path    

def getPathTo(start, end, Map, goThroughWalls = 0, diagonal=3, ignoreRestricted=True):
    cost = np.array(Map.tiles["passable"], dtype=np.int8)
    if goThroughWalls:
        cost[np.where(cost==0)]=goThroughWalls
    if ignoreRestricted:
        cost[np.where(Map.restricted)]=0
    graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=diagonal)
    pathfinder = tcod.path.Pathfinder(graph)
    pathfinder.add_root(start)
    return pathfinder.path_to(end).tolist()[1:]


def areaCollides(entityPositionComponent, otherPositionComponent):
    return (
        entityPositionComponent['x'] < otherPositionComponent['x'] + otherPositionComponent['width']
            and entityPositionComponent['x'] + entityPositionComponent['width'] >= otherPositionComponent['x']
            and entityPositionComponent['y'] < otherPositionComponent['y'] + otherPositionComponent['height']
            and entityPositionComponent['y'] + entityPositionComponent['height'] >= otherPositionComponent['y']
    )

def pointCollides(entityPositionComponent, x, y):
    return (
        x >= entityPositionComponent['x']
        and x < entityPositionComponent['x'] + entityPositionComponent['width']
        and y >= entityPositionComponent['y']
        and y < entityPositionComponent['y'] + entityPositionComponent['height']
    )