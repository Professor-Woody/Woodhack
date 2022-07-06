from Components.Components import Initiative, Position, Render
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
        self.map = None

    def update(self):
        for entity in self.world.create_query(all_of=[Initiative]).result:
            entity.fire_event('tick')

        for entity in self.world.entities:
            entity.fire_event('update')

        self.map.update()

        self.map.draw(self.app.screen)

        for entity in self.world.create_query(all_of=[Render, Position]).result:
            entity.fire_event('render', {'level': self})


class GameLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        self.map=LevelCreator.generateBasicLevel(self, self.width-30, self.height-10)

        self.entityManager.loadEntities("objects.json")
        self.entityManager.spawn("PLAYER", self.map.start[0], self.map.start[1])
        # self.entityManager.spawn("torch", self.map.start[0], self.map.start[1]-1)
        # self.entityManager.spawn("orc", self.map.start[0]+2, self.map.start[1])
        # self.entityManager.spawn("shortsword", self.map.start[0], self.map.start[1])
        # self.entityManager.spawn("orc", self.map.start[0]+1, self.map.start[1]+2)
        # self.entityManager.spawn("orc", self.map.start[0]+1, self.map.start[1]-2)

        self.map.update()

