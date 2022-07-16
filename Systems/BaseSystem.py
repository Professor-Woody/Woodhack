class BaseSystem:
    def __init__(self, level):
        self.level = level
        self._actionQueue = []

    def post(self, action):
        self._actionQueue.append(action)

    @property
    def actionQueue(self):
        for action in self._actionQueue:
            yield action
        self._actionQueue.clear()