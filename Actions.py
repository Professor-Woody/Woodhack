class Action:
    def __init__(self):
        pass

    def perform(self):
        print (f"why are you performing {type(self)}?")


class EntityAction(Action):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity




class KeyAction(Action):
    def __init__(self, key, state, app):
        super().__init__()
        self.key = key
        self.state = state
        self.app = app

    def perform(self):
        self.app.keyboardController.setKey(self.key, self.state)
    



class ActionWithDirection(EntityAction):
    def __init__(self, entity, dx, dy):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy


class MovementAction(ActionWithDirection):
    def perform(self):
        dx = self.entity.x + self.dx
        dy = self.entity.y + self.dy

        if not self.entity.level.map.checkInBounds(dx, dy):
            return
        if not self.entity.level.map.checkIsPassable(dx, dy):
            return
        if self.entity.level.entityManager.checkIsBlocked(dx, dy):
            return
        self.entity.move(dx, dy)

class CheerAction(EntityAction):
    def __init__(self, entity, msg):
        super().__init__(entity)
        self.msg = msg

    def perform(self):
        print (self.msg)
        WaitAction(self.entity, 60).perform()


class WaitAction(EntityAction):
    def __init__(self, entity, time):
        super().__init__(entity)
        self.time = time
    
    def perform(self):
        print(f"{self.entity.type} is waiting")
        self.entity.speed += self.time

class WatchAction(WaitAction):
    def __init__(self, entity, time):
        super().__init__(entity, time)
    
    def perform(self):
        self.entity.target = None
        if self.entity.level.map.checkIsVisible(self.entity):
            for player in self.entity.level.entityManager.players:
                if player == self.entity:
                    continue
                if not self.entity.target:
                    self.entity.target = player
                else:
                    if self.getDistance(player) < self.getDistance(self.entity.target):
                        self.entity.target = player
        else:
            super().perform()        
    
    def getDistance(self, target):
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        return max(abs(dx, abs(dy)))