from Helpers.LevelCreation import floor, generators
import Helpers.PositionHelper as PositionHelper



class Biome:
    genType = "caverns"

    def __init__(self):
        pass

    def createBaseMap(self, gameMap):
        # here we use the designated algorithms to build the base tunnels/rooms
        generators[self.genType](gameMap)





    def createStartRoom(self, gameMap, startSpot):
        if not startSpot:
            dist = 0
            startSpot = gameMap.pointsOfInterest[0]
            endSpot = None

            for poi in gameMap.pointsOfInterest[1:]:
                rng = PositionHelper.getRange(startSpot, poi)
                if rng > dist:
                    endSpot = poi
                    dist = rng
        
        drawShape(startSpot, 'circle3', floor, gameMap)
        
        gameMap.startSpot = startSpot
        gameMap.endSpot = endSpot



    def createRooms(self, gameMap):
        # create required prefabs
        for key in self.requiredPrefabs:
            # a prefab held in the levelCreator
            # it has the following information:
            #   it's shape (a list of tuples containing coords and tile type)
            #   (optional) entry/exit connector points which need pathing to them
            #   (optional) a list of spawnpoints for entities
            
            self.creator.prefabs[key].createRoom(
                self.tileset, #the tiles for this biome (so we can theme properly)
                gameMap
            )


        # create optional prefabs (amount based on number 
        # provided with biome)



        # create random rooms (amount, type, and min/max size
        # provided with biome)


    def spawnEntities(self, level):
        pass

    def createExitRoom(self, gameMap):
        drawShape(gameMap.endSpot, 'square2', floor, gameMap)