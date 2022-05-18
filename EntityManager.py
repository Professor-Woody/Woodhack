class EntityManager:
    entityTypes = {}
    breedTypes = {}
    allEntities = set()

    def add(self, entity):
        self.allEntities.add(entity)

    def remove(self, entity):
        if entity in self.allEntities:
            self.allEntities.remove(entity)

    def checkIsBlocked(self, movingEntity):
        for entity in self.allEntities:
            if entity.blocksMovement:
                if movingEntity.x == entity.x and movingEntity.y == entity.y:
                    return entity
        return None

    def update(self, level):
        for entity in self.allEntities:
            entity.update(level)

    def draw(self, map, screen):
        for entity in self.entities:
            if map.checkIsVisible(entity):
                screen.draw(entity)


    # TODO: Replace both of these with an xml parser
    def loadEntities(self, filename):
        with open(filename) as entityDefs:
            reader = csv.reader(entityDefs, delimiter=',')
            readHeader = False
            for row in reader:
                if not readHeader:
                    readHeader = True
                else:
                    self.entityTypes[row[0]] = Entity(row[1], (row[2], row[3], row[4]), row[5])

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
        self.entityTypes[entityName].spawn(self, x, y)



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