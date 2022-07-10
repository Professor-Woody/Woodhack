from Components.Components import Initiative, Position, Render
from EntityManager import EntityManager
from Levels.LevelCreator import LevelCreator
from ecstremity import ECSEvent
import time

class BaseLevel:
    lastTime = time.time()*1000
    fps = 0
    lastFps = 0
    
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        self.bottomX = 0
        self.sideY = 0

        self.world = self.app.ecs.create_world()
        self.entityManager = EntityManager(self)
        self.map = None

        self.tickQuery = self.world.create_query(all_of=['Initiative'], store_query='tick')
        self.renderItemsQuery = self.world.create_query(all_of=['IsItem', 'Render', 'Position'], store_query='renderItems')
        self.renderActorsQuery = self.world.create_query(all_of=['Render', 'Position'], any_of=['IsNPC', 'IsPlayer'], none_of=['IsItem'], store_query='renderActors')
        self.renderUIQuery = self.world.create_query(all_of=['IsUI', 'Position'], store_query='renderUI')
        self.collisionQuery = self.world.create_query(all_of=['Position', 'Collision'], store_query='collidable')

        self.world.create_query(store_query='update')
        self.world.create_query(any_of=['IsPlayer', 'IsNPC'], store_query='actors')
        self.world.create_query(all_of=['IsPlayer'], store_query='players')
        self.world.create_query(all_of=['IsNPC'], store_query='NPCs')
        self.world.create_query(all_of=['IsItem'], store_query='items')
        self.world.create_query(all_of=['IsDead'], store_query='dead')
        

    def update(self):
        self.world.post(ECSEvent('tick', target='tick'))
        self.world.post(ECSEvent('update', target='update'))
        self.world.update()

        self.entityManager.update()
        if self.world.updateMap:
            self.map.update()
            self.world.updateMap = False

        self.map.draw(self.app.screen)

        for entity in self.renderItemsQuery.result:
            entity.fire_event('render', {'level': self})
        for entity in self.renderActorsQuery.result:
            entity.fire_event('render', {'level': self})
        for entity in self.renderUIQuery.result:
            entity.fire_event('render', {'level': self})


        self.fps += 1
        curTime = time.time()*1000
        if curTime >= self.lastTime + 1000:
            self.lastTime = curTime
            self.lastFps = self.fps
            self.fps = 0
        self.app.screen.printLine(0, 0, str(self.lastFps))
        self.app.screen.printLine(0, 1, str(len(self.renderActorsQuery.result)))



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

