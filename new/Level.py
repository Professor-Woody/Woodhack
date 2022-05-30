from EntityManager import EntityManager

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


class GameLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)
        print ("GameLevel")