import Colours as colour

class BaseSystem:
    actions = None
    def __init__(self, level):
        self.level = level
        self._actionQueue = []
        if self.actions:
            self.level.registerSystem(self.actions, self)

    def post(self, action):
        self._actionQueue.append(action)

    @property
    def actionQueue(self):
        try:
            for action in self._actionQueue:
                yield action
        finally:
            self._actionQueue.clear()

    def getComponents(self, component):
        return self.level.e.component.components[component]

    def log(self, message, colour=colour.WHITE):
        self.level.post('log', {'colour': colour, 'message': message})

    def clog(self, message, colour=colour.WHITE):
        self.level.post('clog', {'colour': colour, 'message': message})        