from dataclasses import dataclass, field
from typing import Tuple
from ecstremity import Component, Engine
from Levels.Maps import GameMap
import Colours as colour
from Flags import FPS
from Controllers import BaseController
from Actions.EntityActions import MovementAction, GetTargetAction

@dataclass
class Position(Component):
    x: int = -1
    y: int = -1
    width: int = 1
    height: int = 1

    def on_move(self, event):
        self.x = event.x
        self.y = event.y


class Collision(Component):
    def areaCollides(self, other):
        return (
            self.entity[Position].x < other.x + other.width
                and self.entity[Position].x + self.entity[Position].width >= other.x
                and self.entity[Position].y < other.y + other.height
                and self.entity[Position].y + self.entity[Position].height >= other.y
        )
    
    def pointCollides(self, x, y):
        return (
            x >= self.entity[Position].x
            and x < self.entity[Position].x + self.entity[Position].width
            and y >= self.entity[Position].y
            and y < self.entity[Position].y + self.entity[Position].height
        )


class Stats(Component):
    def __init__(self, hp):
        self.hp = hp
        self.maxHp = hp


@dataclass
class Light(Component):
    radius: int = 0

@dataclass
class Render(Component):
    map: GameMap = None
    entityName: str = "Bob"
    char: str = "@"
    fg: Tuple = colour.WHITE
    bg: Tuple = None
    needsVisibility: bool = True

    def on_draw(self, event):
        if (self.map.checkIsVisible(self) and self.needsVisibility) or not self.needsVisibility:
            print (event.screen)
            event.screen.draw(self)

    @property
    def x(self):
        return self.entity[Position].x
    
    @property
    def y(self):
        return self.entity[Position].y

    def on_set_bg(self, event):
        self.bg = event.bg

    def on_clear_bg(self, event=None):
        self.bg = None



class Initiative(Component):
    ready: True
    speed: int = 0

    def on_add_initiative(self, event):
        self.speed += event.speed
        self.ready = False

    def on_tick(self, event):
        if self.speed > 0:
            self.speed -= 1
            return            
        self.ready = True



class Targeted(Component):
    targetCycleSpeed = 0
    targetCycleIndex = 0
    targetedBy: list = field(default_factory=lambda: [])

    def on_update(self, event):
        if self.targetedBy: # we're being targeted
            self.targetCycleSpeed -= 1

            if self.targetCycleSpeed <= 0:  # change to next colour
                self.targetCycleSpeed = FPS / 2
                self.targetCycleIndex -= 1
                if self.targetCycleIndex < 0:
                    self.targetCycleIndex = len(self.targetedBy)-1
                self.entity.fire_event('set_bg', {'bg': self.targetedBy[Render].bg})

    def on_add_targeter(self, event):
        if event.entity not in self.targetedBy:
            self.targetedBy.append(event.entity)
            self.targetCycleSpeed = 0
    
    def on_remove_targeter(self, event):
        if event.entity in self.targetedBy:
            self.targetedby.remove(event.entity)
            self.targetCycleSpeed = 0
            if not self.targetedBy:
                self.entity.fire_event('set_bg', {'bg': None})

@dataclass
class PlayerInput(Component):
    controller: BaseController

    def on_update(self, event):
        if self.entity[Initiative].ready:
            # check menu

            
            # check movement
            dx = 0
            dy = 0
            if self.controller.getPressed("up"):
                dy -= 1
            if self.controller.getPressed("down"):
                dy += 1
            if self.controller.getPressed("left"):
                dx -= 1
            if self.controller.getPressed("right"):
                dx += 1

            if dx or dy:
                MovementAction(self, dx, dy, 6).perform()            

            # check use actions (IE equipment)



            # check targetting
            target = None
            if self.controller.getPressedOnce("next"):
                target = "next"
            elif self.controller.getPressedOnce("previous"):
                target = "previous"
            elif self.controller.getPressedOnce("nearestEnemy"):
                target = "nearestEnemy"
            
            if target:
                GetTargetAction(self, target).perform()


class Player(Component):
    pass


class UI(Component):
    pass

def registerComponents(ecs: Engine):
    components = [
        Position,
        Collision,
        Light,
        Render,
        Initiative,
        Targeted,
        PlayerInput,
        Stats,
        Player,
        UI,
    ]
    for component in components:
        ecs.register_component(component)