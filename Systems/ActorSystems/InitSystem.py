from Systems.BaseSystem import BaseSystem
from Components import *

class InitSystem(BaseSystem):
    actions=['add_speed']
    priority = 0
    active = True

    def post(self, action):
        self._actionQueue.append(action)
        if not self.active:
            self.level.activateSystem(self.priority)
            self.active = True

    def run(self):
        # add speed to any from actions
        initComponents = self.level.e.component.components[Init]
        if self._actionQueue:

            for action in self.actionQueue:
                initComponents[action['entity']]['speed'] += action['speed']
                if initComponents[action['entity']]['speed'] > initComponents[action['entity']]['maxSpeed']:
                    initComponents[action['entity']]['maxSpeed'] = initComponents[action['entity']]['speed']
                self.level.e.removeComponent(action['entity'], IsReady)
        
        # now update everyone 
        entities = self.level.initQuery.result
        if entities:
            for entity in entities:
                initComponents[entity]['speed'] = max(0, initComponents[entity]['speed']-1)
                if initComponents[entity]['speed'] <= 0:
                    self.level.e.addComponent(entity, IsReady)
                    initComponents[entity]['speed'] = 0
                    initComponents[entity]['maxSpeed'] = 0
        else:
            self.level.deactivateSystem(self.priority)
            self.active = False
