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
        player = Player(self.map.start[0], self.map.start[1], "@", WHITE, self.keyboardController)

        self.entityManager = EntityManager()
        self.entityManager.loadEntities('npcs.csv')
        self.entityManager.add(player)

        self.entityManager.spawn('orc', player.x+1, player.y)


    def update(self):
        self.map.update(self.entityManager.players)
        self.entityManager.update(self)


    def draw(self, screen):
        self.map.draw(screen)
        
        self.entityManager.draw(self.map, screen)