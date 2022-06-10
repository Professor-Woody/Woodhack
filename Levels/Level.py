from EntityManager import EntityManager
from Levels.LevelCreator import LevelCreator

class BaseLevel:
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        self.bottomX = 0
        self.sideY = 0

        self.world = self.app.ecs.create_world()
        self.entityManager = EntityManager(self)

    def update(self):
        self.entityManager.update()

    def draw(self, screen):
        self.entityManager.draw(screen)





class GameLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)
        print ("GameLevel")

        self.map=LevelCreator.generateBasicLevel(self, self.width, self.height)

        self.entityManager.loadEntities("npcs.csv")
        self.entityManager.spawn("orc", self.map.start[0]-1, self.map.start[1])
        self.entityManager.spawn("orc", self.map.start[0]+1, self.map.start[1])
        self.entityManager.spawn("Woody", self.map.start[0], self.map.start[1])
        # self.entityManager.spawn("orc", self.map.start[0]+5, self.map.start[1])
        # self.entityManager.spawn("orc", self.map.start[0]+1, self.map.start[1]+2)
        # self.entityManager.spawn("orc", self.map.start[0]+1, self.map.start[1]-2)

    def update(self):
        self.map.update()
        super().update()

    def draw(self, screen):
        self.map.draw(screen)
        super().draw(screen)