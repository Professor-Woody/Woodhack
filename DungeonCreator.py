import numpy as np
from Rooms import RectangularRoom, floor, wall, SHROUD
from tcod.map import compute_fov
import random
import tcod
from Maps import GameMap


class DungeonCreator:
    minRoomSize = 2
    maxRoomSize = 12
    maxRooms = 10

    @classmethod
    def giveMeADungeon(cls, width, height):
        dungeon = GameMap(width, height)

        lastRoom = None
        rooms = []

        for x in range(cls.maxRooms):
            room = cls.createRoom(width, height)
            
            if any(room.intersects(other) for other in rooms):
                continue           
            
            rooms.append(room)

            if lastRoom:

                for x, y in cls.createTunnel(room.center, lastRoom.center):
                    dungeon.tiles[x, y] = floor
                dungeon.end = room.center
            else:
                lastRoom = room
                dungeon.start = room.center
            
            dungeon.tiles[room.inner] = floor

        return dungeon

    @classmethod
    def createRoom(cls, mapWidth, mapHeight):
        width = random.randint(2, 20)
        height = random.randint(2, 20)
        x = random.randint(1, mapWidth - width - 1)
        y = random.randint(1, mapHeight - height - 1)
        return RectangularRoom(x, y, width, height)


    @classmethod
    def createTunnel(cls, start, end):
        x1, y1 = start
        x2, y2 = end

        if random.randint(0,1):
            cornerX, cornerY = x2, y1
        else:
            cornerX, cornerY = x1, y2
        
        for x, y in tcod.los.bresenham((x1, y1), (cornerX, cornerY)).tolist():
            yield x, y
        for x, y in tcod.los.bresenham((cornerX, cornerY), (x2, y2)).tolist():
            yield x, y

