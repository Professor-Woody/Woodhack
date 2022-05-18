import numpy as np
from Rooms import RectangularRoom, floor, wall
from tcod.map import computer_fov
import random

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = np.full((self.width, self.height), fill_value=wall, order="F")
        self.visible = np.full((self.width, self.height), fill_value=False, order="F")
        self.explored = np.full((self.width, self.height), fill_value=False, order="F")

        self.start = None
        self.end = None


    def checkIsPassable(self, x, y):
        return self.tiles["passable"][x, y]


    def checkInBounds(self, x, y):
        return 0 <= x < self.map.width and 0 <= y < self.map.height


    def update(self, players):
        # update FOV
        for player in players:
            self.visible[:] = computer_fov(
                self.tiles["transparent"],
                (player.x, player.y),
                radius=8,
            )
        self.explored |= self.visible


    def draw(self, screen):
        screen.drawArray(
            (0,self.width), 
            (0,self.height),
            np.select(
                condlist=[self.visible, self.explored],
                choicelist=[self.tiles["light"], self.tiles["dark"]],
                default=SHROUD
                )
        )




class DungeonCreator:
    minRoomSize = 2
    maxRoomSize = 12
    maxRooms = 10

    @classmethod
    def giveMeADungeon(cls, width, height):
        dungeon = GameMap(width, height)

        lastRoom = None
        rooms = []

        for x in range(maxRooms):
            room = cls.createRoom(width, height)
            
            if any(room.intersects(other) for other in rooms):
                continue           
            
            rooms.append(room)

            if lastRoom:
                for x, y in createTunnel(room.center, lastRoom.center):
                    dungeon.tiles[x, y] = floor
                dungeon.end = room.center()
            else:
                lastRoom = room
                dungeon.start = room.center()
            
            dungeon.tiles[room] = floor

        return dungeon

    @classmethod
    def createRoom(cls, mapWidth, mapHeight):
        width = random.randint(2, 20)
        height = random.randint(2, 20)
        x = random.randint(1, mapWidth - width - 1)
        y = random.randint(1, mapHeight - height - 1)
        return RectangularRoom(x, y, x+width, y+height)


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

