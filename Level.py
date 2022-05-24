from Controllers import JoystickController
from DungeonCreator import DungeonCreator
from Player import Player
from EntityManager import EntityManager
import Colours as colour
import Controllers
from UI import Button
from Actions import PrintAction

class BaseLevel:
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height

        self.entityManager = EntityManager(self)

    def update(self):
        self.entityManager.update()
    
    def draw(self, screen):
        self.entityManager.draw(screen)


class MainMenu(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        button = Button(self, 10, 10, 7, 3, "test", PrintAction("test button pressed"))
        self.entityManager.add(button)



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
        self.entityManager.draw(screen)