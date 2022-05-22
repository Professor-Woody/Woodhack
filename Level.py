from DungeonCreator import DungeonCreator
from Player import Player
from EntityManager import EntityManager
import Colours as colour

class Level:
    def __init__(self, app, width, height):
        self.app = app

        self.width = width
        self.height = height

        self.map = DungeonCreator.giveMeADungeon(self.width-40, self.height-10)

        player = Player(self.map.start[0], self.map.start[1], "@", colour.WHITE, self.app.keyboardController, self)

        self.entityManager = EntityManager(self)
        self.entityManager.loadEntities('npcs.csv')
        self.entityManager.add(player)

        self.entityManager.spawn('orc', self.map.end[0], self.map.end[1])
        self.entityManager.spawn('orc', self.map.end[0]+1, self.map.end[1])
        self.entityManager.spawn('orc', self.map.end[0]-1, self.map.end[1])
        self.entityManager.spawn('orc', self.map.end[0], self.map.end[1]+1)
        self.entityManager.spawn('orc', self.map.end[0], self.map.end[1]-1)


    def update(self):
        self.map.update(self.entityManager.players)
        self.entityManager.update()


    def draw(self, screen):
        self.map.draw(screen)
        
        self.entityManager.draw(self.map, screen)