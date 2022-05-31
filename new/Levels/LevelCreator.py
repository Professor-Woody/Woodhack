from Levels.Rooms import RectangularRoom, floor
import random
import tcod
from Levels.Maps import GameMap


class LevelCreator:
    minRoomSize = 2
    maxRoomSize = 12
    maxRooms = 20

    @classmethod
    def generateBasicLevel(cls, level, width, height):
        gameMap = GameMap(level, width, height)

        lastRoom = None
        rooms = []

        for x in range(cls.maxRooms):
            room = cls.createRoom(width, height)
            
            if any(room.intersects(other) for other in rooms):
                continue           
            
            rooms.append(room)

            if lastRoom:

                for x, y in cls.createTunnel(room.center, lastRoom.center):
                    gameMap.tiles[x, y] = floor
                gameMap.end = room.center
            else:
                lastRoom = room
                gameMap.start = room.center
            
            gameMap.tiles[room.inner] = floor

        return gameMap

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

