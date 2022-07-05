import os
import importlib

class BaseSystem:
    def __init__(self, systemsManager, path=None):
        self.systemsManager = systemsManager
        self.actionQueue = []

        self.actions = {}

        if path:
            self.registerSubSystems(path)
    
    def registerSubSystems(self, path):
        for module in os.listdir(os.path.join(os.getcwd(), 'Systems/' + path)):
            if module == '__init__.py' or module[-3:] != '.py':
                continue
            importlib.import_module('Systems.' + path + '.' + module[:-3]).SubSystem(self)


    def register(self, action, subSystem):
        self.actions[action] = subSystem


    def run(self):
        for action in self.actionQueue:
            self.actions[type(action)].run(action)
        self.actionQueue.clear()


    def post(self, action):
        self.actionQueue.append(action)

    @property
    def level(self):
        return self.systemsManager.level

