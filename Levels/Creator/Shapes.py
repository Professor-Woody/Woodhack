surrounding = [
    (-1,-1), (0,-1), (1, -1),
    (-1,0), (1,0),
    (-1,1), (0,1), (1,1)
    ]

square = [(0,0), (-1, -1), (-1, 0), (0,-1)]
square2 = [(x-1,y-1) for x in range(3) for y in range(3)] 
square2.pop(4)
square3 = [(x-2,y-2) for x in range(5) for y in range(5)] 
square3.pop(12)
square4 = [(x-2,y-2) for x in range(7) for y in range(7)]
square5 = [(x-2,y-2) for x in range(9) for y in range(9)]

diamond2 = [(0,-1),(-1, 0), (1, 0),(0, 1)]
diamond3 = [(0, -2),(-1, -1), (0, -1), (1, -1),(-2, 0), (-1, 0), (1, 0), (2, 0),(-1, 1), (0, 1), (1, 1),(0, 2)]
circle3 = [(-1, -2), (0, -2), (1, -2),(-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),(-2, 0), (-1, 0), (1, 0), (2, 0),(-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),(-1, 2), (0, 2), (1, 2),]

shapes = {
    'surrounding': surrounding,
    'square': square,
    'square2': square2,
    'square3': square3,
    'square4': square4,
    'square5': square5,
    'diamond2': diamond2,
    'diamond3': diamond3,
    'circle3': circle3
}


def drawShape(pos, shape, biome, tileType, gameMap):
    for (dx,dy) in shapes[shape]:
        x = pos[0] + dx
        y = pos[1] + dy
        gameMap.tiles[x,y] = biome.getTile(tileType)
