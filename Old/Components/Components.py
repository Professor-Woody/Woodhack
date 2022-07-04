from dataclasses import dataclass
from typing import Tuple
from ecstremity import Component, Engine, Entity
from Levels.Maps import GameMap
import Colours as colour
from Flags import FPS
from Controllers import BaseController
from Actions.PlayerActions import GetPlayerInputAction
import tcod

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
    
    def getRange(self, other):
        return max(abs(self.x - other[Position].x), abs(self.y - other[Position].y))

    def getLOS(self, other):
        path = tcod.los.bresenham(
            (self.x, self.y),
            (other[Position].x, other[Position].y)
        ).toList()

        for x, y in path:
            if not self.level.map.checkIsPassable(x,y) or self.level.map.checkIsBlocked(x, y):
                return False
        return True

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

    def on_damage(self, event):
        damage = max(event.data.damage, 0)
        self.hp -= damage
        print (f"{self.entity[Render].entityName} took {damage} damage")
        if self.hp <= 0:
            print (f"oh snap, {self.entity[Render].entityName} is dead")
            self.entity.add(EffectControlsLocked)
        if not self.entity[Target].target:
            self.entity[Target].target = event.data.entity

@dataclass
class Light(Component):
    radius: int = 0

@dataclass
class Render(Component):
    entityName: str = "Bob"
    char: str = "@"
    fg: Tuple = colour.WHITE
    bg: Tuple = None
    needsVisibility: bool = True

    def on_draw(self, event):
        if self.entity.has(Position):
            if (self.entity[Position].level.map.checkIsVisible(self.entity) and self.needsVisibility):
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

class IsReady(Component):
    pass

class Initiative(Component):
    speed: int = 0

    def on_add_initiative(self, event):
        if self.entity.has(IsReady):
            self.entity.remove(IsReady)
        if not self.entity.has(Cooldown):
            self.entity.add(Cooldown, {'speed': event.data.speed})
        else:
            self.entity[Cooldown] += event.data.speed


class Cooldown(Component):
    speed: int = 0
    def on_tick(self, event):
        if self.speed > 0:
            self.speed -= 1
            return
        if not self.ready:
            self.entity.add(IsReady)
            self.entity.remove(self)


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
    controller: any

    def on_update(self, event):
        self.controller.update()
        if not self.entity.has(EffectControlsLocked):
            event.data.actions.append(GetPlayerInputAction(self.entity))

class IsPlayer(Component):
    pass

class IsNPC(Component):
    pass

class IsItem(Component):
    pass

@dataclass
class IsEquipped(Component):
    parentEntity: Entity

@dataclass
class IsEquippable(Component):
    equipmentSlot: str

class Inventory(Component):
    def __init__(self):
        self.contents = []

class EffectControlsLocked(Component):
    pass

class Body(Component):
    def __init__(self):
        self.equipmentSlots = {
            'head': None,
            'lefthand': None,
            'righthand': None,
            'body': None,
            'legs': None,
            'Feet': None
        }




