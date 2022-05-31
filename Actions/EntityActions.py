from Actions.Actions import Action


class EntityAction(Action):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity


class WaitAction(EntityAction):
    def __init__(self, entity, time):
        super().__init__(entity)
        self.time = time

    def perform(self):
        self.entity.speed += self.time


class CheerAction(EntityAction):
    def __init__(self, entity, msg):
        super().__init__(entity)
        self.msg = msg

    def perform(self):
        print(self.msg)


class WatchAction(WaitAction):
    def perform(self):
        print (self.entity.name + "is watching")
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


class MovementAction(EntityAction):
    def __init__(self, entity, dx, dy, speed):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy
        self.speed = speed

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
            self.entity.move(self.entity.x + self.dx, self.entity.y + self.dy)
            self.entity.speed += self.speed

    def checkCanMove(self, dx, dy):
        if not self.entity.level.map.checkInBounds(dx, dy) or \
            not self.entity.level.map.checkIsPassable(dx, dy) or \
            self.entity.level.entityManager.checkIsBlocked(dx, dy):
            return False
        return True

class GetTargetAction(EntityAction):
    def __init__(self, entity, targetRange):
        super().__init__(entity)
        self.targetRange = targetRange

    def perform(self):
        targets = []
        currentTargetIndex = -1

        for actor in self.entity.level.entityManager.actors:
            if actor.level.map.checkIsVisible(actor):
                targetRange = max(abs(self.entity.x - actor.x), abs(self.entity.y - actor.y))
                targets.append((actor, targetRange))

        targets.sort(key = lambda x: x[1])
        
        counter = 0
        for actor in targets:
            if actor[0] == self.entity.target:
                currentTargetIndex = counter
                break
            counter += 1

        if targets:
            if self.targetRange == "next":
                currentTargetIndex += 1
                if currentTargetIndex > len(targets)-1:
                    currentTargetIndex = 0
            elif self.targetRange == "previous":
                currentTargetIndex -= 1
                if currentTargetIndex < 0:
                    currentTargetIndex = len(targets)-1
            else:
                currentTargetIndex = 0

            
            if self.entity.target:
                self.entity.target.targettedBy.remove(self.entity)

            self.entity.target = targets[currentTargetIndex][0]
            self.entity.target.targettedBy.append(self.entity)
            self.entity.target.targetCycleSpeed = 0
        else:
            if self.entity.target:
                self.entity.target.targettedBy.remove(self.entity)
            self.entity.target = None

        print (f"Player {self.entity}\nis now targetting {self.entity.target}\nfrom list {targets}")
