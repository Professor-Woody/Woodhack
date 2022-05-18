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

        self.keyboardController = KeyboardController()    # there's only 1 keyboard per computer    
        player = Player(self.map.start[0], self.map.start[1], "@", WHITE, self.app, self.keyboardController)

        self.entityManager = EntityManager()
        self.entityManager.loadEntities('npcs.csv')
        self.entityManager.add(player)

        self.entityManager.spawn('orc', 20, 20)


    def update(self):
        self.entityManager.update(self)


    def draw(self, screen):
        self.map.draw(screen)
        
        self.entityManager.draw(self.map, screen)