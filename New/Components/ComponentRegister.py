from ecstremity import Engine

import inspect
import Components.Components
import Components.FlagComponents
import Components.UIComponents
import Components.ItemComponents

components = []
components += [obj for name,obj in inspect.getmembers(Components.Components) if inspect.isclass(obj) and name != 'Component']
components += [obj for name,obj in inspect.getmembers(Components.FlagComponents) if inspect.isclass(obj) and name != 'Component']
components += [obj for name,obj in inspect.getmembers(Components.UIComponents) if inspect.isclass(obj) and name != 'Component']
components += [obj for name,obj in inspect.getmembers(Components.ItemComponents) if inspect.isclass(obj) and name != 'Component']
def registerComponents(ecs: Engine):
    for component in components:
        ecs.register_component(component)