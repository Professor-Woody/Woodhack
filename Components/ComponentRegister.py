from ecstremity import Engine, Component

import inspect
import Components.Components
import Components.FlagComponents
import Components.TargetComponents
import Components.UIComponents
import Components.InventoryComponents
import Components.ItemComponents
import Components.AIComponents

components = []
components += [obj for name,obj in inspect.getmembers(Components.Components) if inspect.isclass(obj) and name != 'Component' and issubclass(obj, Component)]
components += [obj for name,obj in inspect.getmembers(Components.FlagComponents) if inspect.isclass(obj) and name != 'Component' and issubclass(obj, Component)]
components += [obj for name,obj in inspect.getmembers(Components.TargetComponents) if inspect.isclass(obj) and name != 'Component' and issubclass(obj, Component)]
components += [obj for name,obj in inspect.getmembers(Components.UIComponents) if inspect.isclass(obj) and name != 'Component' and issubclass(obj, Component)]
components += [obj for name,obj in inspect.getmembers(Components.InventoryComponents) if inspect.isclass(obj) and name != 'Component' and issubclass(obj, Component)]
components += [obj for name,obj in inspect.getmembers(Components.ItemComponents) if inspect.isclass(obj) and name != 'Component' and issubclass(obj, Component)]
components += [obj for name,obj in inspect.getmembers(Components.AIComponents) if inspect.isclass(obj) and name != 'Component' and issubclass(obj, Component)]
def registerComponents(ecs: Engine):
    for component in components:
        ecs.register_component(component)