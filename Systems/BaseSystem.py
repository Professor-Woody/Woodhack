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
        if action not in self.actions.keys():
            self.actions[action] = []
        self.actions[action].append(subSystem)


    def run(self):
        for action in self.actionQueue:
            for subSystem in self.actions[type(action)]:
                subSystem.run(action)
        self.actionQueue.clear()


    def post(self, action):
        self.actionQueue.append(action)

    @property
    def level(self):
        return self.systemsManager.level

