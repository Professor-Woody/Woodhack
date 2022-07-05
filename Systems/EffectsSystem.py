from Components.Components import Light
from Systems.BaseSystem import BaseSystem
from Actions.EffectsActions import RecalculateStatsAction
from Components.Components import Body, Light
import os
import importlib

class EffectsSystem(BaseSystem):
    def __init__(self, systemsManager):
        super().__init__(systemsManager)

        self.actions = {
        }

        self.registerSubSystems()
    
    def registerSubSystems(self):
        for module in os.listdir(os.path.join(os.getcwd(), 'Systems/SubSystems')):
            if module == '__init__.py' or module[-3:] != '.py':
                continue
            importlib.import_module('Systems.SubSystems.' + module[:-3]).SubSystem(self)


    def register(self, action, subSystem):
        self.actions[action] = subSystem

    def run(self):
        for action in self.actionQueue:
            print ('yyyy')
            print (type(action))
            print (self.actions)
            self.actions[type(action)].run(action)
        self.actionQueue.clear()


