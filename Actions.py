
class ActionManager:
    def __init__(self):
        self.actionQueue = []

    def add(self, action):
        self.actionQueue.append(action)

    def getActions(self):
        queue = self.actionQueue.copy()
        self.actionQueue = []
        return queue



class Action:
    def __init__(self):
        pass

    def perform(self, level):
        print (f"why are you performing {type(self)}?")

class EntityAction(Action):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity




class KeyAction(Action):
    def __init__(self, key, state):
        super().__init__()
        self.key = key
        self.state = state

    def perform(self, level):
        level.keyboardController.setKey(self.key, self.state)
    



class ActionWithDirection(EntityAction):
    def __init__(self, entity, dx, dy):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy


class MovementAction(ActionWithDirection):
    def perform(self, level):
        dx = self.entity.x + self.dx
        dy = self.entity.y + self.dy

        print(1)
        if not level.map.checkInBounds(dx, dy):
            print (2)
            return
        print (3)
        if not level.map.checkIsPassable(dx, dy):
            print (4)
            return 
        print (5)
        if level.entityManager.checkIsBlocked(dx, dy):
            print (6)
            return
        print(7)
        self.entity.move(dx, dy)

class CheerAction(EntityAction):
    def __init__(self, entity, msg):
        super().__init__(entity)
        self.msg = msg

    def perform(self, level):
        print (self.msg)