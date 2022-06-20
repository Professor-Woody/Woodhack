from ecstremity import Component
import Colours as colour
from typing import Tuple
from dataclasses import dataclass

@dataclass
class Render(Component):
    entityName: str = "Bob"
    char: str = "@"
    fg: Tuple = colour.WHITE
    bg: Tuple = None
    needsVisibility: bool = True


@dataclass
class Position(Component):
    x: int = -1
    y: int = -1
    width: int = 1
    height: int = 1
    level: any = None

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
            self.entity[Position].x < other.x + other.width
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


@dataclass
class Collision(Component):
    pass


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

@dataclass
class Stats(Component):
    def __init__(self, hp, moveSpeed, defence, attack, bonusDamage):
        self.hp = hp
        self.maxHp = hp
        self.baseMaxHp = hp
        self.baseMoveSpeed = moveSpeed
        self.moveSpeed = moveSpeed
        self.baseDefence = defence
        self.defence = defence
        self.baseAttack = attack
        self.attack = attack
        self.baseAttack = attack
        self.bonusDamage = bonusDamage
        self.baseBonusDamage = bonusDamage

    @property
    def moveSpeed(self):
        return self._moveSpeed
    @moveSpeed.setter
    def moveSpeed(self, value):
        self._moveSpeed = max(2, value)

    @property   
    def baseMoveSpeed(self):
        return self._baseMoveSpeed
    @baseMoveSpeed.setter
    def baseMoveSpeed(self, value):
        self._baseMoveSpeed = max(2, value)        

    def on_recalculate_stats(self, event):
        
        self.maxHp = 
