import numpy as np
import tcod
from tcod.map import compute_fov
from Components import *
from random import randint
import Helpers.PositionHelper as PositionHelper
from Levels.Creator.Tiles import SHROUD, newTile, tile_dt


class GameMap:
    def __init__(self, level, width, height):
        self.level = level
        self.width = width
        self.height = height
        self.tiles = np.empty((self.width, self.height), dtype=tile_dt, order="F")
        self.lit = np.full((self.width, self.height), fill_value=False, order="F")
        self.visible = np.full((self.width, self.height), fill_value=False, order="F")
        self.explored = np.full((self.width, self.height), fill_value=False, order="F")
        self.restricted = np.full((self.width, self.height), fill_value=False, order="F")

        self.startPoint = None
        self.exitPoint = None
        self.POIs = []

    def getPOI(self):
        return self.POIs.pop(randint(0, len(self.POIs)-1))


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

