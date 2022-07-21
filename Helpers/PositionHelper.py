import tcod

def getRange(entityCoords, otherCoords):
    return max(abs(entityCoords[0] - otherCoords[0]), abs(entityCoords[1] - otherCoords[1]))


def getLOS(entity, other, visionRange, Map):
    path = tcod.los.bresenham(
        (entity[0], entity[1]),
        (other[0], other[1])
    ).tolist()
    if len(path)-1 > visionRange:
        return False

    for x, y in path[1:-1]:
        if not Map.checkIsPassable(x,y) \
            or Map.checkIsBlocked(x, y):
            return False
    return path      

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