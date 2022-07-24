from Systems.BaseSystem import BaseSystem
from Components import *

class InitSystem(BaseSystem):
    actions=['add_speed']
    def run(self):
        
        initComponents = self.level.e.component.components[Init]

        for action in self.actionQueue:
            initComponents[action['entity']]['speed'] += action['speed']
            if initComponents[action['entity']]['speed'] > initComponents[action['entity']]['maxSpeed']:
                initComponents[action['entity']]['maxSpeed'] = initComponents[action['entity']]['speed']
            self.level.e.removeComponent(action['entity'], IsReady)
        
        entities = self.level.initQuery.result
        for entity in entities:
            initComponents[entity]['speed'] = max(0, initComponents[entity]['speed']-1)
            if initComponents[entity]['speed'] <= 0:
                self.level.e.addComponent(entity, IsReady)
                initComponents[entity]['speed'] = 0
                initComponents[entity]['maxSpeed'] = 0

        
