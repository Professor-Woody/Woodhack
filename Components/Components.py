from dataclasses import dataclass, field
from typing import Tuple
from ecstremity import Component, Engine, Entity
from Levels.Maps import GameMap
import Colours as colour
from Flags import FPS
from Controllers import BaseController
from Actions.EntityActions import GetSelectionInput, GetPlayerInputAction

@dataclass
class Position(Component):
    x: int = -1
    y: int = -1
    width: int = 1
    height: int = 1
    level: any = None

    def on_move(self, event):
        self.x = event.data.x
        self.y = event.data.y

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

class BlocksMovement(Component):
    pass

@dataclass
class UIPosition(Component):
    sideX: int
    sideY: int
    bottomX: int
    bottomY: int


class Target(Component):
    target: Entity = None
    def on_set_target(self, event):
        self.target = event.data.target

    def on_clear_target(self, event):
        if self.target:
            self.target.fire_event("remove_targeter", {"entity": self.entity})


class Stats(Component):
    def __init__(self, hp, moveSpeed):
        self.hp = hp
        self.maxHp = hp
        self.moveSpeed = moveSpeed


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
        if self.entity.has(Position):
            if (self.map.checkIsVisible(self.entity) and self.needsVisibility):
                event.data.screen.draw(self)
            if not self.needsVisibility:
                event.data.screen.draw(self)

    @property
    def x(self):
        return self.entity[Position].x
    
    @property
    def y(self):
        return self.entity[Position].y

    def on_set_bg(self, event):
        self.bg = event.data.bg

    def on_clear_bg(self, event=None):
        self.bg = None



class Initiative(Component):
    ready: bool = False
    speed: int = 0

    def on_add_initiative(self, event):
        self.speed += event.data.speed
        self.ready = False

    def on_tick(self, event):
        if self.speed > 0:
            self.speed -= 1
            return
        if not self.ready:
            self.ready = True



class Targeted(Component):
    targetCycleSpeed = 0
    targetCycleIndex = 0
    def __init__(self):
        self.targetedBy = []

    def on_update(self, event):
        if self.targetedBy: # we're being targeted
            self.targetCycleSpeed -= 1

            if self.targetCycleSpeed <= 0:  # change to next colour
                self.targetCycleSpeed = FPS / 2
                self.targetCycleIndex -= 1
                if self.targetCycleIndex < 0:
                    self.targetCycleIndex = len(self.targetedBy)-1
                self.entity.fire_event('set_bg', {'bg': self.targetedBy[self.targetCycleIndex][Render].fg})

    def on_add_targeter(self, event):
        if event.data.entity not in self.targetedBy:
            self.targetedBy.append(event.data.entity)
            self.targetCycleSpeed = 0
    
    def on_remove_targeter(self, event):
        print (f"removing {event.data.entity}")
        if event.data.entity in self.targetedBy:
            self.targetedBy.remove(event.data.entity)
            self.targetCycleSpeed = 0
            if not self.targetedBy:
                self.entity.fire_event('set_bg', {'bg': None})

@dataclass
class PlayerInput(Component):
    controller: BaseController

    def on_update(self, event):
        self.controller.update()
        if self.entity[Initiative].ready and not self.entity.has(EffectControlsLocked):
            event.data.actions.append(GetPlayerInputAction(self.entity))

class IsPlayer(Component):
    pass

class IsNPC(Component):
    pass

class IsItem(Component):
    pass

class IsEquipped(Component):
    pass

class UI(Component):
    pass

class Inventory(Component):
    def __init__(self):
        self.contents = []

class EffectControlsLocked(Component):
    pass

class SelectionUI(Component):
    def __init__(self, parentEntity, items, actions):
        self.parentEntity = parentEntity
        self.items = items
        self.choice = 0
        self.actions = actions

    def on_update(self, event):
        event.data.actions.append(GetSelectionInput(self.entity))

    def on_draw(self, event):
        screen = event.data.screen
        screen.drawFrame(
            self.entity[Position].x,
            self.entity[Position].y,
            self.entity[Position].width,
            self.entity[Position].height,
            "Pick up:"
        )
        for i in range(min(len(self.entity['SelectionUI'].items), 10)):
            if i == self.choice:
                screen.printLine(self.entity[Position].x+2, self.entity[Position].y+i+1, self.entity['SelectionUI'].items[i][Render].entityName, fg=colour.BLACK, bg=colour.WHITE)
            else:
                screen.printLine(self.entity[Position].x+2, self.entity[Position].y+i+1, self.entity['SelectionUI'].items[i][Render].entityName)

class EquipmentSlot(Component):
    equipped = None

class LeftHand(EquipmentSlot):
    pass

class RightHand(EquipmentSlot):
    pass

def registerComponents(ecs: Engine):
    components = [
        Position,
        Collision,
        Light,
        Render,
        Initiative,
        Target,
        Targeted,
        PlayerInput,
        Stats,
        IsPlayer,
        IsNPC,
        IsItem,
        IsEquipped,
        UI,
        SelectionUI,
        EffectControlsLocked,
        LeftHand,
        RightHand,
        BlocksMovement,
        SelectionUI,

    ]
    for component in components:
        ecs.register_component(component)