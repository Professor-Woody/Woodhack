import numpy as np


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



class RectangularRoom:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x2 = x + width
        self.y2 = y + height


    @property
    def center(self):
        """return centre of room"""
        centerX = int((self.x + self.x2) / 2)
        centerY = int((self.y + self.y2) / 2)

        return centerX, centerY
    
    @property
    def inner(self):
        """return inner area as a 2d array index"""
        return slice(self.x + 1, self.x2), slice(self.y + 1, self.y2)

    def intersects(self, other):
        return (
            self.x <= other.x2
            and self.x2 >= other.x
            and self.y < other.y2
            and self.y2 >= other.y
        )