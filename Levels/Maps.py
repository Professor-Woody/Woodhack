import numpy as np
from Levels.Rooms import wall, SHROUD
import tcod
from tcod.map import compute_fov
from Components import *
import Helpers.PositionHelper as PositionHelper

class GameMap:
    def __init__(self, level, width, height):
        self.level = level
        self.width = width
        self.height = height
        self.tiles = np.full((self.width, self.height), fill_value=wall, order="F")
        self.lit = np.full((self.width, self.height), fill_value=False, order="F")
        self.visible = np.full((self.width, self.height), fill_value=False, order="F")
        self.explored = np.full((self.width, self.height), fill_value=False, order="F")

        self.startSpot = None
        self.endSpot = None


    def checkIsPassable(self, x, y):
        return self.tiles["passable"][x, y]

    def checkInBounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def checkIsVisible(self, x, y):
        return self.visible[x, y]# and self.lit[x, y]

    def checkIsBlocked(self, x, y):
        positionComponents = self.level.e.component.components[Position]

        for entity in self.level.collidableQuery.result:
            if PositionHelper.pointCollides(positionComponents[entity], x, y):
                return entity
        return False

    def update(self):
        # calculate lit squares
        self.lit[:] = False

        entities = self.level.lightsQuery.result
        positionComponents = self.level.e.component.filter(Position, entities)
        lightComponents = self.level.e.component.filter(Light, entities)

        for entity in entities:
            self.lit += compute_fov(
                    self.tiles["transparent"],
                    (positionComponents[entity]['x'], positionComponents[entity]['y']),
                    radius=lightComponents[entity]['radius'],
                    algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST
                )
            

        # calculate visible squares from lit
        entities = self.level.playersQuery.result
        positionComponents = self.level.e.component.filter(Position, entities)

        self.visible[:] = False
        for entity in entities:
            self.visible += np.logical_and(self.lit, compute_fov(
                        self.tiles["transparent"],
                        (positionComponents[entity]['x'], positionComponents[entity]['y']),
                        radius=40,
                        algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST
                    )
                )
        self.explored |= self.visible



    def draw(self, screen):
        screen.drawArray(
            (0,self.width), 
            (0,self.height),
            np.select(
                condlist=[self.visible, self.explored],
                choicelist=[self.tiles["light"], self.tiles["dark"]],
                default=SHROUD
                )
        )

