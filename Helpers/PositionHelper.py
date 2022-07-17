import tcod

def getRange(entityCoords, otherCoords):
    return max(abs(entityCoords[0] - otherCoords[0]), abs(entityCoords[1] - otherCoords[1]))


def getLOS(entity, other, Map):
    path = tcod.los.bresenham(
        (entity[0], entity[1]),
        (other[0], other[1])
    ).tolist()
    for x, y in path[1:-1]:
        if Map.checkIsPassable(x,y) \
            or Map.checkIsBlocked(x, y):
            return False
    return True      