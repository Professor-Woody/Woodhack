import tcod
from Actions import Action
import numpy as np

class BaseComponent:
    entity = None

    @property
    def level(self):
        return self.entity.level



class Breed(BaseComponent):
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




class BaseAI(Action, BaseComponent):
    def getPathTo(self, dx, dy):
        cost = np.array(self.entity.level.map.tiles["walkable"], dtype=np.int8)

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

