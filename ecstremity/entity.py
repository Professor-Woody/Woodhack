from __future__ import annotations
from typing import *
from collections import OrderedDict

from ecstremity.component import ComponentMeta

from ecstremity.bit_util import *
from ecstremity.entity_event import EntityEvent, EventData

from ecstremity.component import Component

if TYPE_CHECKING:
    from ecstremity.world import World


def attach_component(entity: Entity, component: Component) -> None:
    entity.components[component.comp_id] = component


def remove_component(entity: Entity, component_name: str) -> None:
    component = entity.components[component_name.upper()]
    del entity.components[component_name.upper()]
    entity.cbits = subtract_bit(entity.cbits, component.cbit)
    entity.candidacy()


def serialize_component(component: Component) -> Dict[str, Any]:
    return component.serialize()


class Entity:

    def __init__(self, world: World, uid: str) -> None:
        self.world = world
        self.uid = uid
        self.components: OrderedDict[str, Component] = OrderedDict()
        self.is_destroyed: bool = False
        self.componentLock: bool = False
        self.addComponentList = []
        self.removeComponentList = []

        self._cbits: int = 0
        self._qeligible: bool = True

    def __getitem__(self, component: Union[Component, str]) -> Component:
        if isinstance(component, ComponentMeta):
            component = component.comp_id
        return self.components[component.upper()]

    def __getstate__(self) -> Dict[str, Any]:
        return {
            "uid": getattr(self, "uid"),
            "components": getattr(self, "components")
        }

    def __setstate__(self, state: Dict[str, Any]) -> None:
        for k, v in state.items():
            setattr(self, k, v)

    def __hash__(self) -> int:
        return int(self.uid)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Entity):
            return (
                self.uid == other.uid and
                self.is_destroyed == other.is_destroyed and
                self._qeligible == other._qeligible and
                self.components == other.components
            )
        return False

    def __repr__(self) -> str:
        component_list = ", ".join(self.components.keys())
        return f"Entity [{self.uid}] with [{component_list}]"

    @property
    def cbits(self) -> int:
        return self._cbits

    @cbits.setter
    def cbits(self, value: int) -> None:
        self._cbits = value

    def candidacy(self) -> None:
        """Check this entity against the existing queries in the active world."""
        if self._qeligible:
            self.world.candidate(self)

    def add(self, component: Union[Component, str], properties: Dict[str, Any] = {}) -> None:
        """Create and add a registered component to the entity initialized with
        the specified properties.
        A component instance can be supplied instead.
        """
        if isinstance(component, str):
            component = self.world.engine.components[component.upper()]
        if "_entity" in properties.keys():
            del properties["_entity"]
        component = component(**properties)
        if not self.componentLock:
            self.attachComponent(component)
        else:
            self.addComponentList.append(component)

    def attachComponent(self, component):
        attach_component(self, component)

        self._cbits = add_bit(self._cbits, component.cbit)
        component._on_attached(self)
        self.candidacy()

    def has(self, component: Union[Component, str]) -> bool:
        """Check if a particular component is currently attached to this Entity."""
        if isinstance(component, str):
            component = self.world.engine.components[component.upper()]
        return has_bit(self._cbits, component.cbit)

    def owns(self, component: Union[Component, str]) -> bool:
        """Check if target component has this entity as an owner."""
        if isinstance(component, str):
            component = self.world.engine.components[component.upper()]
        return component.entity == self

    def remove(self, component):
        """Remove a component from the entity."""
        if isinstance(component, str) and self.has(component):
            if not self.componentLock:
                self.removeComponent(component)
            else:
                self.removeComponentList.append(component)
        else:
            if self.has(component.comp_id):
                if not self.componentLock:
                    self.removeComponent(component.comp_id)
                else:
                    self.removeComponentList.append(component.comp_id)

    def removeComponent(self, component):
        remove_component(self, component)

    def destroy(self) -> None:
        """Destroy this entity and all attached components."""
        to_destroy = []
        for name, component in self.components.items():
            to_destroy.append(component)

        for component in to_destroy:
            self.remove(component)
            component._on_destroyed()

        self.world.destroyed(self.uid)
        self.components.clear()
        self.is_destroyed = True

    def serialize(self) -> Dict[str, Union[str, Dict[str, Any]]]:
        components: Dict[str, Any] = {}
        for comp_id in self.components.keys():
            component_state = self.components[comp_id].__getstate__()
            components[comp_id] = component_state
        return {
            "uid": self.uid,
            "components": components
        }

    def fire_event(self, name: str, data: Optional[Union[Dict[str, Any], EventData]] = None, tryFirst = False) -> EntityEvent:
        """Fire an event to all Components attached to this Entity."""
        if isinstance(data, EventData):
            data = data.get_record()
        if not data:
            data = {}
        data['failed'] = False
        
        if tryFirst:
            name = 'try_' + name
        
        evt = EntityEvent(name, data)
        self.componentLock = True
        for i in range(1+int(tryFirst)):
            for component in self.components.values():
                component._on_event(evt)
                if evt.prevented:
                    evt.data.failed = True
                    break
            if evt.data.failed:
                break
            evt.name = name.strip("try_")
        
        self.componentLock = False
        for component in self.addComponentList:
            self.attachComponent(component)
        self.addComponentList.clear()
        for component in self.removeComponentList:
            self.removeComponent(component)
        self.removeComponentList.clear()

        return evt
