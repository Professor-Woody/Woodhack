import Colours as colour

class BaseSystem:
    actions = None
    priority = 1000000
    alwaysActive = True

    def __init__(self, level):
        self.level = level
        self._actionQueue = []
        self.level.registerSystem(self.priority, self, self.alwaysActive)

        if self.actions:
            self.level.registerActions(self.priority, self.actions)
            

    def post(self, action):
        self._actionQueue.append(action)
        if not self.alwaysActive:
            self.level.activateSystem(self.priority)

    @property
    def actionQueue(self):
        try:
            for action in self._actionQueue:
                yield action
        finally:
            self._actionQueue.clear()
            if not self.alwaysActive:
                self.level.deactivateSystem(self.priority)

    def getComponents(self, component):
        return self.level.e.component.components[component]

    def hasComponent(self, entity, component):
        return self.level.e.hasComponent(entity, component)

    def log(self, message, colour=colour.WHITE):
        self.level.post('log', {'colour': colour, 'message': message})

    def clog(self, message, colour=colour.WHITE):
        self.level.post('clog', {'colour': colour, 'message': message})        