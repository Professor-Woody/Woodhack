from ecstremity import Engine, Entity, World


class WHWorld(World):
    def add(self, entity: Entity) -> None:
        self._entities[entity.uid] = entity

    def remove(self, entity: Entity) -> None:
        if entity.uid in self._entities.keys():
            self._entities.pop(entity.uid)


class WHEngine(Engine):
    def create_world(self) -> WHWorld:
        return WHWorld(self)