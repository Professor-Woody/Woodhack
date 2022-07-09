from dataclasses import dataclass
from Components.FlagComponents import IsReady
from ecstremity import Component
import Colours as colour
from typing import Tuple
import tcod
from random import choice

class Render(Component):
    def __init__(self, 
                entityName: str = "Bob", 
                char: str = "@", 
                fg: Tuple = choice(colour.COLOURS),
                bg: Tuple = None,
                needsVisibility: bool = True):
        self.entityName = entityName
        self.char = char
        self.fg = fg
        self.bg = bg
        self.baseBG = bg
        self.needsVisibility = needsVisibility

    def on_render(self, action):
        if self.entity.has(Position):
            if self.needsVisibility:
                if action.data.level.map.checkIsVisible(self.entity):
                    action.data.level.app.screen.draw(self.entity)
            else:
                action.data.level.app.screen.draw(self.entity)



@dataclass
class Position(Component):
    x: int = -1
    y: int = -1
    width: int = 1
    height: int = 1
    level: any = None

    def on_move(self, action):
        dx = action.data.dx
        dy = action.data.dy
        newLocationX = self.x + dx
        newLocationY = self.y + dy

        if self.checkCanMove(newLocationX, newLocationY):
            pass
        else:
            if not self.checkCanMove(newLocationX, self.y):
                dx = 0
            if not self.checkCanMove(self.x, newLocationY):
                dy = 0
        if dx or dy:
            self.x += dx
            self.y += dy


    def checkCanMove(self, dx, dy):
        if not self.level.map.checkInBounds(dx, dy) or \
            not self.level.map.checkIsPassable(dx, dy) or \
            self.level.map.checkIsBlocked(dx, dy):
            return False
        return True


    @staticmethod    
    def getRange(entity, other):
        return max(abs(entity[Position].x - other[Position].x), abs(entity[Position].y - other[Position].y))

    @staticmethod   
    def getLOS(entity, other):
        path = tcod.los.bresenham(
            (entity[Position].x, entity[Position].y),
            (other[Position].x, other[Position].y)
        ).toList()

        for x, y in path:
            if not entity[Position].level.map.checkIsPassable(x,y) or entity[Position].level.map.checkIsBlocked(x, y):
                return False
        return True                


class Collision(Component):
    @staticmethod
    def areaCollides(entity, other):
        return (
            entity[Position].x < other.x + other.width
                and entity[Position].x + entity[Position].width >= other.x
                and entity[Position].y < other.y + other.height
                and entity[Position].y + entity[Position].height >= other.y
        )
    
    @staticmethod
    def pointCollides(entity, x, y):
        return (
            x >= entity[Position].x
            and x < entity[Position].x + entity[Position].width
            and y >= entity[Position].y
            and y < entity[Position].y + entity[Position].height
        )


class Light(Component):
    def __init__(self, radius = 3):
        self.radius = radius
        self.baseRadius = radius


@dataclass
class Initiative(Component):
    speed: int = 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = max(0, value)

    def on_add_speed(self, action):
        self.speed += action.data.speed
        if self.entity.has(IsReady):
            self.entity.remove(IsReady)

    def on_tick(self, action):
        self.speed -= 1
        if not self.speed and not self.entity.has(IsReady):
            self.entity.add(IsReady)

@dataclass
class Stats(Component):
    hp: int = 10
    maxHp: int = 10
    moveSpeed: int = 6
    baseMoveSpeed: int = 6
    attack: int = 0
    defence: int = 0
    bonusDamage: int = 0


    def on_recalculate_stats(self, action):
        print ("recalculating stats")

        # recalculating light
        self.entity[Light].radius = self.entity[Light].baseRadius
        
        for key in self.entity['Body'].slots.keys():
            slot = self.entity['Body'].slots[key]
            print (key, slot)
            if slot and slot.has(Light) and slot[Light].radius > self.entity[Light].radius:
                self.entity[Light].radius = slot[Light].radius
                print (f"new light radius: {self.entity[Light].radius}")
                