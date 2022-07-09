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

        self.tickQuery = self.world.create_query(all_of=['Initiative'], store_query=True)
        self.renderItemsQuery = self.world.create_query(all_of=['IsItem', 'Render', 'Position'], store_query=True)
        self.renderActorsQuery = self.world.create_query(all_of=['Render', 'Position'], any_of=['IsNPC', 'IsPlayer'], none_of=['IsItem'], store_query=True)
        self.renderUIQuery = self.world.create_query(all_of=['IsUI', 'Position'], store_query=True)


    def update(self):
        for entity in self.tickQuery.result:
            entity.fire_event('tick')

        for entity in self.world.entities:
            entity.fire_event('update')

        self.entityManager.update()
        self.map.update()

        self.map.draw(self.app.screen)

        for entity in self.renderItemsQuery.result:
            entity.fire_event('render', {'level': self})
        for entity in self.renderActorsQuery.result:
            entity.fire_event('render', {'level': self})
        for entity in self.renderUIQuery.result:
            entity.fire_event('render', {'level': self})



class GameLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        self.map=LevelCreator.generateBasicLevel(self, self.width-30, self.height-10)

        self.entityManager.loadEntities("objects.json")
        self.entityManager.spawn("PLAYER", self.map.start[0], self.map.start[1])

        # self.entityManager.spawn("torch", self.map.start[0], self.map.start[1]-1)
        self.entityManager.spawn("orc", self.map.start[0]+2, self.map.start[1])
        # self.entityManager.spawn("shortsword", self.map.start[0], self.map.start[1])
        # self.entityManager.spawn("orc", self.map.start[0]+1, self.map.start[1]+2)
        # self.entityManager.spawn("orc", self.map.start[0]+1, self.map.start[1]-2)

        self.map.update()

