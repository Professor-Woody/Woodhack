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
    

class PrintAction(Action):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def perform(self):
        print(self.msg)




class ActionWithDirection(EntityAction):
    def __init__(self, entity, dx, dy, time=10):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy
        self.time = time


class MovementAction(ActionWithDirection):
    def perform(self):
        # first check if we can diagonally move
        newLocationX = self.entity.x + self.dx
        newLocationY = self.entity.y + self.dy
        if self.checkCanMove(newLocationX, newLocationY):
            print ("option A")
            pass

        # if not then do our best single axis movement
        else:
            if not self.checkCanMove(newLocationX, self.entity.y):
                self.dx = 0
                print ("option B")

            if not self.checkCanMove(self.entity.x + self.dx, newLocationY):
                print ("option C")
                self.dy = 0


        if self.dx or self.dy:
            self.entity.move(self.dx, self.dy)
            self.entity.speed += self.time

    def checkCanMove(self, dx, dy):
        if not self.entity.level.map.checkInBounds(dx, dy) or \
            not self.entity.level.map.checkIsPassable(dx, dy) or \
            self.entity.level.entityManager.checkIsBlocked(dx, dy):
            return False
        return True

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
        self.entity.speed += self.time

class WatchAction(WaitAction):
    def __init__(self, entity, time):
        super().__init__(entity, time)
    
    def perform(self):
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
            if not self.entity.target:
                super().perform()        
    
    def getDistance(self, target):
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        return max(abs(dx, abs(dy)))