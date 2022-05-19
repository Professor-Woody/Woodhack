from DungeonCreator import DungeonCreator
from Player import Player
from EntityManager import EntityManager
from Controllers import KeyboardController

WHITE = (255, 255, 255)

class Level:
    def __init__(self, app, width, height):
        self.app = app

        self.width = width
        self.height = height

        self.map = DungeonCreator.giveMeADungeon(self.width, self.height)

        player = Player(self.map.start[0], self.map.start[1], "@", WHITE, self.app.keyboardController, self)

        self.entityManager = EntityManager(self)
        self.entityManager.loadEntities('npcs.csv')
        self.entityManager.add(player)

        self.entityManager.spawn('orc', self.map.end[0], self.map.end[1])


    def update(self):
        self.map.update(self.entityManager.players)
        self.entityManager.update()


    def draw(self, screen):
        self.map.draw(screen)
        
        self.entityManager.draw(self.map, screen)