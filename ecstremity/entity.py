from __future__ import annotations
from typing import *
from collections import OrderedDict

from ecstremity.component import ComponentMeta

from ecstremity.bit_util import *
from ecstremity.entity_event import EntityEvent, EventData, ECSEvent

from ecstremity.component import Component

if TYPE_CHECKING:
    from ecstremity.world import World


def attach_component(entity: Entity, component: Component) -> None:
    if entity.has(component) and component.allow_multiple:
        entity[component].multiple += 1
    else:
        entity.components[component.comp_id] = component


def remove_component(entity: Entity, component_name: str) -> None:
    if entity.is_destroyed:
        print (f"Entity already destroyed: {entity}, {component_name}")
        return
    component = entity.components[component_name.upper()]
    if component.allow_multiple:
        component.multiple -= 1
    if (component.allow_multiple and component.multiple <= 0) or not component.allow_multiple:
        del entity.components[component_name.upper()]


def serialize_component(component: Component) -> Dict[str, Any]:
    return component.serialize()


class Entity:

    def __init__(self, world: World, uid: str) -> None:
        self.world = world
        self.uid = uid
        self.components: OrderedDict[str, Component] = OrderedDict()
        self.is_destroyed: bool = False
        self._componentLock: int = 0
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
    def componentLock(self) -> int:
        return self._componentLock

    @componentLock.setter
    def componentLock(self, value: int) -> None:
        self._componentLock = max(0, value)

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
        compName = ""
        if isinstance(component, str):
            compName = component
            component = self.world.engine.components[component.upper()]
        else:
            compName = component.comp_id
        
        if self.has(compName):
            if not self.componentLock:
                self.removeComponent(component)
            else:
                self.removeComponentList.append(component)
    

    def removeComponent(self, component):
        if self.has(component):
            remove_component(self, component.comp_id)
            self._cbits = subtract_bit(self._cbits, component.cbit)
            self.candidacy()

        else:
            print (f"Remove Component Miss: {component}")



    def destroy(self) -> None:
        """Destroy this entity and all attached components."""
        to_destroy = []

        for name, component in self.components.items():
            to_destroy.append(component)
        for component in to_destroy:
            self.removeComponent(component)
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


    def post(self, event: Union[ECSEvent, str], data=None, target=None):
        if not isinstance(event, ECSEvent):
            if isinstance(data, EventData):
                data = data.get_record()
            if not data:
                data = {}
            event = ECSEvent(event, data, target)
        event.source = self
        self.world.post(event)



    def fire(self, event):
        self.componentLock += 1
        if event.tryFirst:
            event.name = 'try_' + event.name

        for i in range(1+int(event.tryFirst)):
            for component in self.components.values():
                component._on_event(event)
                if event.prevented:
                    break
            if event.prevented:
                break
            if event.tryFirst:
                event.name = event.name[4:]
        self.componentLock -= 1

        if not self.componentLock:
            for component in self.addComponentList:
                self.attachComponent(component)
            self.addComponentList.clear()
            for component in self.removeComponentList:
                self.removeComponent(component)
            self.removeComponentList.clear()





    def fire_event(self, name: str, data: Optional[Union[Dict[str, Any], EventData]] = None, tryFirst = False) -> EntityEvent:
        """Fire an event to all Components attached to this Entity."""
        if self.is_destroyed:
            print (f"event {name} {data} ignored. {self} already destroyed")
        if isinstance(data, EventData):
            data = data.get_record()
        if not data:
            data = {}
        data['failed'] = False
        
        if tryFirst:
            name = 'try_' + name
        
        evt = EntityEvent(name, data)
        self.componentLock += 1
        for i in range(1+int(tryFirst)):
            for component in self.components.values():
                component._on_event(evt)
                if evt.prevented:
                    evt.data.failed = True
                    break
            if evt.data.failed:
                break
            evt.name = name.strip("try_")
        
        self.componentLock -= 1

        if not self.componentLock:
            for component in self.addComponentList:
                self.attachComponent(component)
            self.addComponentList.clear()
            for component in self.removeComponentList:
                self.removeComponent(component)
            self.removeComponentList.clear()

        return evt
