from Components.Components import Collision, Position, Render
from Components.FlagComponents import IsReady
from Components.TargetComponents import Target
from ecstremity import Component
import numpy as np
import tcod

from ecstremity.entity_event import ECSEvent

class BaseAI(Component):
    def on_update(self, action):
        if self.entity.has(IsReady):
            print (f"{self.entity[Render].entityName} is waiting")
            self.entity.post('add_speed', {'speed':60})


    def getPathTo(self, dx, dy):
        cost = np.array(self.entity[Position].level.map.tiles["passable"], dtype=np.int8)
        for entity in self.entity[Position].level.collisionQuery.result:
            if entity != self.entity and entity.has(Collision) and cost[entity[Position].x, entity[Position].y]:
                # add to cost of a blocked position
                # there's a potential for the entity to move out so we still
                # count it as a possible path.

                # a lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player
                cost[entity[Position].x, entity[Position].y] += 10
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)
        pathfinder.add_root((self.entity[Position].x, self.entity[Position].y))
        path = pathfinder.path_to((dx, dy))[1:].tolist()
        result = [(index[0], index[1]) for index in path]
        return result

class HostileAI(BaseAI):
    def __init__(self):
        super().__init__()
        self.path = []

    def on_update(self, action):
        if self.entity.has(IsReady):
            target = self.entity[Target].target
        
            if target:
                dx = target[Position].x - self.entity[Position].x
                dy = target[Position].y - self.entity[Position].y
                distance = max(abs(dx), abs(dy))
                if self.entity[Position].level.map.visible[self.entity[Position].x, self.entity[Position].y]:
                    if distance <= 1:
                        self.entity.post(ECSEvent('add_speed', {'speed':30}))
                        return             
                if distance < 8:
                    self.path = self.getPathTo(target[Position].x, target[Position].y)
                if self.path:
                    destx, desty = self.path.pop(0)
                    self.entity.post('move_ip', {'dx': destx, 'dy': desty})
                    self.entity.post(ECSEvent('add_speed', {'speed':20}))
                    return

            self.entity.post(ECSEvent('add_speed', {'speed':120}))


class TargeterAI(Component):
    preyType = "IsPlayer"
    speed = 0

    def on_update(self, action):
        self.speed -= 1
        if self.speed <= 0:
            self.speed = 60
            if not self.entity[Target].target:
                targets = []
                for otherEntity in self.entity.world.create_query(all_of=[self.preyType]).result:
                    if Position.getLOS(self.entity, otherEntity):
                        targetRange = Position.getRange(self.entity, otherEntity)
                        targets.append((otherEntity, targetRange))
                
                targets.sort(key = lambda x: x[1])

                if targets:
                    self.entity[Target].target = targets[0][0]
            else:
                if not Position.getLOS(self.entity, self.entity[Target].target) \
                    and not self.entity[HostileAI].path:
                    self.entity[Target].target = None
