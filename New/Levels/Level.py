from EntityManager import EntityManager
from Levels.LevelCreator import LevelCreator
from Systems.RenderSystem import RenderSystem
from Systems.UpdateSystem import UpdateSystem

class BaseLevel:
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        self.bottomX = 0
        self.sideY = 0

        self.world = self.app.ecs.create_world()
        self.entityManager = EntityManager(self)

        self.map = None



    def runSystems(self):
        self.systemsManager.runSystems()


class GameLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)
        print ("GameLevel")

        self.map=LevelCreator.generateBasicLevel(self, self.width-30, self.height-10)

        self.entityManager.loadEntities("objects.json")
        self.entityManager.spawn("PLAYER", "Woody", self.map.start[0], self.map.start[1])
        # self.entityManager.spawn("torch", self.map.start[0], self.map.start[1]-1)
        # self.entityManager.spawn("orc", self.map.start[0]+5, self.map.start[1])
        # self.entityManager.spawn("orc", self.map.start[0]+1, self.map.start[1]+2)
        # self.entityManager.spawn("orc", self.map.start[0]+1, self.map.start[1]-2)

