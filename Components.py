import tcod
from Actions import CheerAction, EntityAction, MovementAction, WatchAction, WaitAction
import numpy as np

class Breed:
    def __init__(self, hp, defense):
        self.maxHp = hp
        self._hp = hp
        self.defense = defense

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.maxHp))




class BaseAI(EntityAction):
    def getPathTo(self, dx, dy):
        cost = np.array(self.entity.level.map.tiles["passable"], dtype=np.int8)

        for entity in self.entity.level.entityManager.allEntities:
            if entity.blocksMovement and cost[entity.x, entity.y]:
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

        return [(index[0], index[1]) for index in path]

    def perform(self):
        return WaitAction(60)

class HostileAI(BaseAI):
    def __init__(self, entity):
        super().__init__(entity)
        self.path = []

    def perform(self):
        target = self.entity.target
        if target:
            dx = target.x - self.entity.x
            dy = target.y - self.entity.y
            distance = max(abs(dx), abs(dy))

            if self.entity.level.map.visible[self.entity.x, self.entity.y]:
                if distance <= 1:
                    return CheerAction(self.entity, f"{self.entity.type} is attacking")

                self.path = self.getPathTo(dx, dy)

            if self.path:
                destx, desty = self.path.pop(0)
                return MovementAction(self.entity, destx-self.entity.x, desty-self.entity.y).perform()
        
        return WatchAction(self.entity, 60).perform()


