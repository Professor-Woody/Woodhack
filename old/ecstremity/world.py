from __future__ import annotations
from typing import *

from uuid import uuid1
from collections import OrderedDict, deque
from collections.abc import ValuesView

from ecstremity.entity import Entity
from ecstremity.event_manager import EventManager
from ecstremity.query import Query
from ecstremity.component import Component

from uuid import UUID

if TYPE_CHECKING:
    from ecstremity.query import QueryType
    from ecstremity.engine import Engine


def deque_filter(
        lst: Deque[Any],
        condition: Callable[..., bool],
        replace: Optional[Callable[[Any], Component]] = None
    ) -> QueryType:
    lst = deque(lst)
    for _ in range(len(lst)):
        item = lst.popleft()
        if condition(item):
            if replace:
                item = replace(item)
            lst.append(item)
    return list(lst)


class World:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine
        self._id = 0
        self._queries: Dict[str: Query] = {}
        self._entities: OrderedDict[str, Entity] = OrderedDict()

        self._entityLock: int = 0
        self.addable_deferred_entities = []
        self.removeable_deferred_entities = []

        self.eventManager = EventManager(self._queries)
        self.updateMap = False

    # Section for managing systems
    # ----------------------------------
    def post(self, event):
        event.world = self
        self.eventManager.post(event)
    
    def update(self):
        self.eventManager.update()

    # ----------------------------------

    def getQuery(self, query):
        return self._queries[query]

    @property
    def entities(self):
        self.entityLock += 1
        for entity in self._entities.values():
            yield entity
        self.entityLock -= 1
        self.add_deferred_entities()
        self.remove_deferred_entities()

    @property
    def entityLock(self) -> int:
        return self._entityLock

    @entityLock.setter
    def entityLock(self, value) -> None:
        self._entityLock = max(0, value)


    def add_deferred_entities(self) -> None:
        if not self.entityLock:
            for entity in self.addable_deferred_entities:
                self._entities[entity.uid] = entity
            self.addable_deferred_entities.clear()

    def remove_deferred_entities(self) -> None:
        if not self.entityLock:
            for entity in self.removeable_deferred_entities:
                try:
                    self._entities.pop(entity.uid)
                except KeyError:
                    pass
            self.removeable_deferred_entities.clear()

    @staticmethod
    def create_uid() -> str:
        return str(uuid1())

    def get_entity(self, uid: str) -> Optional[Entity]:
        return self._entities.get(uid)

    def create_entity(self, uid: Optional[str] = None) -> Entity:
        if not uid:
            uid = self.create_uid()
        assert uid is not None
        entity = Entity(self, uid)
        if not self.entityLock:
            self._entities[uid] = entity
        else:
            self.addable_deferred_entities.append(entity)
        return entity

    def destroy_entity(self, uid: str) -> None:
        entity = self._entities[uid]
        if entity:
            entity.destroy()

    def destroy_entities(self) -> None:
        """Destroy all entities in the world."""
        to_destroy: List[Entity] = []
        entities: ValuesView[Entity] = self._entities.values()
        for entity in entities:
            _entity: Optional[Entity] = self.get_entity(entity.uid)
            if _entity is not None:
                to_destroy.append(_entity)
        for entity in to_destroy:
            entity.destroy()

    def destroy(self) -> None:
        """Muahahaha!"""
        self.destroy_entities()
        self._id = 0
        self._queries = {}
        self._entities = OrderedDict()

    def create_query(
            self,
            any_of: Optional[Deque[str]] = None,
            all_of: Optional[Deque[str]] = None,
            none_of: Optional[Deque[str]] = None,
            store_query: str = None
        ) -> Query:

        # ANY OF
        if any_of and isinstance(any_of[0], str):
            _any_of: QueryType = deque_filter(
                any_of,
                (lambda i: isinstance(i, str)),
                (lambda i: self.engine.components[i.upper()]))
        else:
            _any_of = []

        # ALL OF
        if all_of and isinstance(all_of[0], str):
            _all_of: QueryType = deque_filter(
                all_of,
                (lambda i: isinstance(i, str)),
                (lambda i: self.engine.components[i.upper()]))
        else:
            _all_of = []

        # NONE OF
        if none_of and isinstance(none_of[0], str):
            _none_of: QueryType = deque_filter(
                none_of,
                (lambda i: isinstance(i, str)),
                (lambda i: self.engine.components[i.upper()]))
        else:
            _none_of = []

        query = Query(self, _any_of, _all_of, _none_of)  # type: ignore
        if store_query:
            self._queries[store_query] = query
        return query

    def candidate(self, entity: Entity) -> None:
        for query in self._queries.values():
            query.candidate(entity)

    def destroyed(self, uid: str) -> None:
        try:
            print (9)
            if not self.entityLock:
                print (10)
                self._entities.pop(uid)
                print (11)
            else:
                print (12)
                self.removeable_deferred_entities.append(self._entities[uid])
                print (13)
        except KeyError:
            pass

    def create_prefab(self, name: str, properties: Optional[Dict[str, Any]] = None, uid: Optional[str] = None):
        if not properties:
            properties = {}
        return self.engine.prefabs.create(self, name, properties, uid)

    def serialize(self, entities: Optional[OrderedDict[str, Entity]] = None) -> Dict[str, Any]:
        json:  List[Dict[str, Union[str, Dict[str, Any]]]] = []  # FIXME: Create a type for this lmao wow
        entities = entities if entities else self._entities
        for entity in entities.values():
            json.append(entity.serialize())
        return {
            "entities": json
        }

    def deserialize(self, data) -> None:
        for entity_data in data["entities"]:
            self._create_or_get_by_uid(entity_data["uid"])

        for entity_data in data["entities"]:
            self.deserialize_entity(entity_data)

    def _create_or_get_by_uid(self, uid: str) -> Entity:
        entity: Optional[Entity] = self.get_entity(uid)
        if entity is not None:
            return entity
        else:
            return self.create_entity(uid)

    def deserialize_entity(self, data: Dict[str, Any]) -> None:
        uid: str = data["uid"]
        components: Dict[str, bytes] = data["components"]
        entity = self._create_or_get_by_uid(uid)
        entity._qeligible = False
        for comp_id, comp_props in components.items():
            entity.add(comp_id, {k: v for k, v in comp_props.items() if k[0] != "_"})
        entity._qeligible = True
        entity.candidacy()
