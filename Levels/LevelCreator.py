from Levels.Biome import Biome
from Levels.Rooms import RectangularRoom, floor, wall
import random
import tcod
from Levels.Maps import GameMap
import copy


class NewLevelCreator:
    biomes = {}
    prefabs = {}
        
    @classmethod
    def generateLevel(cls, level, width, height, biomeType, startSpot = None):
        treasureSpots = []
        monsterSpots = []
        exitSpots = []

        # if needed biome not in biomes.keys()
            # load biome json
        if biomeType not in cls.biomes.keys():
            cls.loadBiome(biomeType)
        biome = copy.deepcopy(cls.biomes[biomeType])



        # if needed prefabs not in prefabs.keys()
            # load prefabs
    

        # generate the base level
        gameMap = GameMap(level, width, height)

        biome.createBaseMap(gameMap)

        # if level doesn't require a specific spot for the start
            # add startPoint based on passed startPoint
        biome.createStartRoom(gameMap, startSpot)

        # drop in required pre-fabs (if called for)
            # prepopulate room with required entities
        biome.createRooms(gameMap)

        # populate level with required entities
        biome.spawnEntities(level)

        # populate exit spot
        biome.createExitRoom(gameMap)

        return gameMap

    @classmethod
    def loadBiome(cls, biomeType):
        biome = Biome()
        cls.biomes[biomeType] = biome



class LevelCreator:
    minRoomSize = 2
    maxRoomSize = 8
    maxRooms = 9

    @classmethod
    def generateBasicLevel(cls, level, width, height):
        gameMap = GameMap(level, width, height)

        lastRoom = None
        rooms = []

        for x in range(cls.maxRooms):
            room = cls.createRoom(width, height)
            
            # if any(room.intersects(other) for other in rooms):
            #     continue           
            
            rooms.append(room)

            if lastRoom:

                for x, y in cls.createTunnel(room.center, lastRoom.center):
                    gameMap.tiles[x, y] = floor
                gameMap.end = room.center
            else:
                lastRoom = room
                gameMap.start = room.center
            
            gameMap.tiles[room.inner] = floor
            # gameMap.tiles[(room.x+1, room.y+1)] = wall
            # gameMap.tiles[(room.x+1, room.y2-1)] = wall
            # gameMap.tiles[(room.x2-1, room.y+1)] = wall
            # gameMap.tiles[(room.x2-1, room.y2-1)] = wall
            

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

