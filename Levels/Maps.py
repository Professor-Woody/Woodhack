import numpy as np
from Levels.Rooms import wall, SHROUD
import tcod
from tcod.map import compute_fov

class GameMap:
    def __init__(self, level, width, height):
        self.level = level
        self.width = width
        self.height = height
        self.tiles = np.full((self.width, self.height), fill_value=wall, order="F")
        self.lit = np.full((self.width, self.height), fill_value=False, order="F")
        self.visible = np.full((self.width, self.height), fill_value=False, order="F")
        self.explored = np.full((self.width, self.height), fill_value=False, order="F")

        self.start = None
        self.end = None


    def checkIsPassable(self, x, y):
        return self.tiles["passable"][x, y]


    def checkInBounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def checkIsVisible(self, entity):
        return self.visible[entity.x, entity.y] and self.lit[entity.x, entity.y]


    def update(self):
        # update FOV
        self.lit[:] = False
        for light in self.level.entityManager.lights:
            self.lit = np.logical_or(self.lit, compute_fov(
                self.tiles["transparent"],
                (light.x, light.y),
                radius=light.lightRadius,
                algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST
                )
            )

        self.visible[:] = False
        for player in self.level.entityManager.players:
            self.visible[:] = np.logical_or(self.visible, np.logical_and(self.lit, compute_fov(
                        self.tiles["transparent"],
                        (player.x, player.y),
                        radius=40,
                        algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST
                    )
                )
            )
        self.explored |= self.visible


    def draw(self, screen):
        screen.drawArray(
            (0,self.width), 
            (0,self.height),
            np.select(
                condlist=[np.logical_and(self.visible, self.lit), self.explored],
                choicelist=[self.tiles["light"], self.tiles["dark"]],
                default=SHROUD
                )
        )

