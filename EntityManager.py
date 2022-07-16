from functools import reduce
from Components import *

def subtract_bit(num: int, bit: int) -> int:
    return num & ~(1 << bit)


def add_bit(num: int, bit: int) -> int:
    return num | (1 << bit)


def has_bit(num: int, bit: int) -> bool:
    return (num >> bit) % 2 != 0


def bit_intersection(n1: int, n2: int) -> int:
    return n1 & n2



class Query:
    def __init__(self, entityManager, allOf=[], anyOf=[], noneOf=[], name=None):
        self.name = name
        self._cache = []
        self.entityManager = entityManager

        self._any = reduce(lambda a, b: add_bit(a, b), anyOf, 0)
        self._all = reduce(lambda a, b: add_bit(a, b), allOf, 0)
        self._none = reduce(lambda a, b: add_bit(a, b), noneOf, 0)

        self.refresh()

    def refresh(self) -> None:
        self._cache = []
        for entity in self.entityManager.entities.keys():
            self.candidate(entity)

    def idx(self, entity: int) -> int:
        try:
            return self._cache.index(entity)
        except ValueError:
            return -1

    def matches(self, entityBits: int) -> bool:
        anyOf = self._any == 0 or bit_intersection(entityBits, self._any) > 0
        allOf = bit_intersection(entityBits, self._all) == self._all
        noneOf = bit_intersection(entityBits, self._none) == 0
        return anyOf & allOf & noneOf

    def candidate(self, entity: int) -> bool:
        idx = self.idx(entity)
        isTracking = idx >= 0
        if self.matches(self.entityManager.entities[entity]):
            if not isTracking:
                print (f"entity {entity} is candidate for {self.name}")
                self._cache.append(entity)
            return True
        
        if isTracking:
            del self._cache[idx]
        return False


    @property
    def result(self):
        return self._cache

    


class Component:
    defaults = {}
    def __init__(self):
        self.components = {}

    def registerComponent(self, component: int, defaults: dict={}):
        self.components[component] = {}
        self.defaults[component] = defaults

    def filter(self, component, entities):
        return {key: self.components[component][key] for key in entities}

    def addComponent(self, entity, component, data):
        if not data:
            data = self.defaults[component]
        self.components[component][entity] = data

    def removeComponent(self, entity, component):
        self.components[component].pop(entity)


class Entity:
    uidCounter = 1000

    @classmethod
    def createEntity(cls):
        cls.uidCounter += 1
        return cls.uidCounter
    


class EntityManager:
    def __init__(self):
        self.component = Component()
        self.entities = {}
        self.queries: dict[str: Query] = {}

    def createEntity(self):
        entity = Entity.createEntity()
        self.entities[entity] = 0
        return entity

    def createQuery(self, allOf=[], anyOf=[], noneOf=[], storeQuery = None):
        query = Query(self, allOf, anyOf, noneOf, storeQuery)
        if storeQuery:
            self.queries[storeQuery] = query
        return query

    def getQuery(self, query):
        return self.queries[query]

    def registerComponent(self, component, data = {}):
        self.component.registerComponent(component, data)

    def addComponent(self, entity, component, data = {}):
        self.component.addComponent(entity, component, data)
        self.entities[entity] = add_bit(self.entities[entity], component)
        self.candidacy(entity)

    def removeComponent(self, entity, component):
        self.component.removeComponent(entity, component)
        self.entities[entity] = subtract_bit(self.entities[entity], component)
        self.candidacy(entity)

    def hasComponent(self, entity, component):
        return has_bit(self.entities[entity], component)

    def candidacy(self, entity):
        for query in self.queries.values():
            query.candidate(entity)