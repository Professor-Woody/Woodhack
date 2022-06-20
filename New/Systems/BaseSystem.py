class BaseSystem:
    def __init__(self, systemsManager):
        self.systemsManager = systemsManager
        self.actionQueue = []

    def post(self, action):
        self.actionQueue.append(action)

    @property
    def level(self):
        return self.systemsManager.level

