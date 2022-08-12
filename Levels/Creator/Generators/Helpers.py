from Levels.Creator.Shapes import surrounding
from EntityManager import add_bit

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
    