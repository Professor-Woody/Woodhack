from Systems.BaseSystem import BaseSystem
from Components import *

class InitSystem(BaseSystem):
    actions=['add_speed']
    def run(self):
        
        initComponents = self.level.e.component.components[Init]

        for action in self.actionQueue:
            initComponents[action['entity']]['speed'] += action['speed']
            self.level.e.removeComponent(action['entity'], IsReady)
        
        entities = self.level.initQuery.result
        for entity in entities:
            initComponents[entity]['speed'] = max(0, initComponents[entity]['speed']-1)
            if not initComponents[entity]['speed']:
                print (f"entity {entity} is ready")
                self.level.e.addComponent(entity, IsReady)

        
