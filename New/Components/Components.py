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

@dataclass
class Light(Component):
    radius: int = 3

@dataclass
class Initiative(Component):
    speed: int = 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = max(0, value)
