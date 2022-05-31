import csv
from Entity import Entity, Actor
from Components import Breed

class EntityManager:
    entityTypes = {}
    breedTypes = {}
    allEntities = set()
    players = set()
    lights = set()
    ui = set()

    def __init__(self, level):
        self.level = level

    def add(self, entity):
        self.allEntities.add(entity)

        if entity.type == "PLAYER":
            self.players.add(entity)
        if entity.lightRadius:
            self.lights.add(entity)
        if entity.ui:
            self.ui.add(entity)

    def remove(self, entity):
        if entity in self.allEntities:
            self.allEntities.remove(entity)
        if entity in self.players:
            self.players.remove(entity)
        if entity in self.lights:
            self.lights.remove(entity)

    def checkIsBlocked(self, dx, dy):
        for entity in self.allEntities:
            if entity.blocksMovement:

                if dx == entity.x and dy == entity.y:
                    return entity
        return None

    def update(self):
        for entity in self.allEntities:
            entity.update()

    def draw(self, screen):
        for entity in self.allEntities:
            entity.draw(screen)


    # TODO: Replace both of these with an xml parser
    def loadEntities(self, filename):
        with open(filename) as entityDefs:
            reader = csv.reader(entityDefs, delimiter=',', quotechar='"')
            readHeader = False
            for row in reader:
                if not readHeader:
                    readHeader = True
                else:
                    if row[1] == "NPC":
                        self.entityTypes[row[0]] = Actor(row[1], row[2], (row[3], row[4], row[5]), row[6], int(row[7]))
                    else:
                        self.entityTypes[row[0]] = Entity(row[1], row[2], (row[3], row[4], row[5]), row[6], int(row[7]))
                        print ("=========")
                        for r in row:
                            print ("---")
                            print (r)
                            print (type(r))


    def loadBreeds(self, filename):
        with open(filename) as breedDefs:    
            reader = csv.reader(breedDefs, delimiter=',')
            readHeader = False
            for row in reader:
                if not readHeader:
                    readHeader = True
                else:
                    if row[0] not in self.breedTypes.keys():
                        self.breedTypes[row[0]] = set()
                    self.breedTypes[row[0]].add(Breed(row[1], row[2], row[3]))
                    

    def spawn(self, entityName, x, y):
        self.entityTypes[entityName].spawn(self.level, x, y)












class EntityManagerOLD:
    allEntities = set()
    blockingEntities = set()
    dynamicEntities = set()
    entities = {}

    def add(self, entity):
        self.allEntities.add(entity)

        if entity.type not in self.entities.keys():
            self.entities[entity.type] = set()
        self.entities[entity.type].add(entity)

        if entity.blocksMovement:
            self.blockingEntities.add(entity)

        if entity.isDynamic:
            self.dynamicEntities.add(entity)


    def remove(self, entity):
        self.allEntities.remove(entity)
        self.entities[entity.type].remove(entity)
        self.blockingEntities.remove(entity)
        self.dynamicEntities.remove(entity)


    def checkIsBlocking(self, movingEntity):
        for entity in self.blockingEntities:
            if movingEntity.x == entity.x and movingEntity.y == entity.y:
                return entity
        return None


    def update(self):
        for entity in self.dynamicEntities:
            entity.update()


    def draw(self, map, screen):
        for entity in self.entities:
            if map.checkIsVisible(entity):
                screen.draw(entity)