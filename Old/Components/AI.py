from Components.Components import Component
from Actions.EntityActions import WaitAction, WatchAction, MovementAction, CheerAction
import numpy as np
import tcod

class BaseAI(Component):
    def getPathTo(self, dx, dy):
        cost = np.array(self.entity.level.map.tiles["passable"], dtype=np.int8)

        for entity in self.entity.level.entityManager.allEntities:
            if entity != self.entity and entity.collider and cost[entity.x, entity.y]:
                # add to cost of a blocked position
                # there's a potential for the entity to move out so we still
                # count it as a possible path.

                # a lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player
                cost[entity.x, entity.y] += 10
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)
        pathfinder.add_root((self.entity.x, self.entity.y))
        path = pathfinder.path_to((dx, dy))[1:].tolist()
        result = [(index[0], index[1]) for index in path]
        return result

    def update(self):
        return WaitAction(self.entity, 60).perform()

class HostileAI(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def update(self):
        target = self.entity.target
        if target:
            dx = target.x - self.entity.x
            dy = target.y - self.entity.y
            distance = max(abs(dx), abs(dy))

            if self.entity.level.map.visible[self.entity.x, self.entity.y]:
                if distance <= 1:
                    WaitAction(self.entity, 60).perform()
                    return CheerAction(self.entity, f"{self.entity.name} is attacking").perform()
            if distance < 8:
                self.path = self.getPathTo(target.x, target.y)

            if self.path:
                destx, desty = self.path.pop(0)
                return MovementAction(self.entity, destx-self.entity.x, desty-self.entity.y, 30).perform()
            return WaitAction(self.entity, 60).perform()
        return WatchAction(self.entity, 60).perform()


