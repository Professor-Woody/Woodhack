from EntityManager import EntityManager, Position, Render
from EntityManager import Component as C
from Levels.LevelCreator import LevelCreator
from Components import *
from Systems.RenderEntitiesSystem import RenderEntitiesSystem
from Controllers import controllers




class BaseLevel:
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        

        self.map = None

        def update(self):
            pass

class TestLevel(BaseLevel):
    mover = 1
    def __init__(self, app, width, height):
        super().__init__(app, width, height)
        
        self.map = LevelCreator.generateBasicLevel(self, self.width-30, self.height-10)

        self.e = EntityManager()

        self.e.registerComponent(Position, {'x': 0, 'y': 0})
        self.e.registerComponent(Render, {'char': '@', 'name': 'Woody', 'fg': (255, 0,0)})
        self.e.registerComponent(Light, {'radius': 3})
        self.e.registerComponent(IsPlayer)
        self.e.registerComponent(IsNPC)
        self.e.registerComponent(IsItem)
        self.e.registerComponent(IsVisible)
        self.e.registerComponent(PlayerInput, {'controller': None})

        self.renderQuery = self.e.createQuery(
            allOf=[Position, Render], 
            anyOf=[IsPlayer, IsVisible],
            storeQuery='Render')

        self.lightsQuery = self.e.createQuery(
            allOf=[Position, Light],
            storeQuery='LightsOnGround'
        )

        self.playersQuery = self.e.createQuery(
            allOf=[IsPlayer],
            storeQuery = 'Players'
        )


        self.player = self.e.createEntity()
        self.e.addComponent(self.player, Position, {'x': 10, 'y': 15})
        self.e.addComponent(self.player, Render)
        self.e.addComponent(self.player, IsPlayer)
        self.e.addComponent(self.player, Light)
        self.e.addComponent(self.player, PlayerInput, {'controller': controllers[0]})


        self.renderEntitiesSystem = RenderEntitiesSystem(self)

        
    def post(self, action):
        # for all related systems post this event
        pass


    def update(self):



        self.map.update()

        self.map.draw(self.app.screen)
        self.renderEntitiesSystem.run()