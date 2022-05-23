from Controllers import JoystickController
from DungeonCreator import DungeonCreator
from Player import Player
from EntityManager import EntityManager
import Colours as colour
import Controllers

class Level:
    def __init__(self, app, width, height):
        self.app = app

        self.width = width
        self.height = height

        self.map = DungeonCreator.giveMeADungeon(self, self.width-40, self.height-10)

        controller1 = JoystickController(Controllers.joysticks[0])
        player = Player(self.map.start[0], self.map.start[1], "@", colour.WHITE, controller1, self)

        self.entityManager = EntityManager(self)
        self.entityManager.loadEntities('npcs.csv')
        self.entityManager.loadEntities('objects.csv')
        self.entityManager.add(player)

        self.entityManager.spawn('orc', self.map.end[0], self.map.end[1])
        self.entityManager.spawn('orc', self.map.end[0]+1, self.map.end[1])
        self.entityManager.spawn('orc', self.map.end[0]-1, self.map.end[1])
        self.entityManager.spawn('orc', self.map.end[0], self.map.end[1]+1)
        self.entityManager.spawn('orc', self.map.end[0], self.map.end[1]-1)
        self.entityManager.spawn('torch', player.x, player.y+1)


    def update(self):
        self.map.update()
        self.entityManager.update()


    def draw(self, screen):
        self.map.draw(screen)
        
        self.entityManager.draw(self.map, screen)