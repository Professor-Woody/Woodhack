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


class MovementAction(Action):
    def __init__(self, position, dx, dy, speed):
        super().__init__()
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.position = position

    def perform(self):
        # first check if we can diagonally move
        newLocationX = self.position.x + self.dx
        newLocationY = self.position.y + self.dy
        if self.checkCanMove(newLocationX, newLocationY):
            print ("option A")
            pass

        # if not then do our best single axis movement
        else:
            if not self.checkCanMove(newLocationX, self.position.y):
                self.dx = 0
                print ("option B")

            if not self.checkCanMove(self.position.x + self.dx, newLocationY):
                print ("option C")
                self.dy = 0

        if self.dx or self.dy:
            self.position.entity.fire_event("move", {"x":self.position.x + self.dx, "y": self.position.y + self.dy})
            self.position.entity.fire_event("add_initiative", {"speed": self.speed})


    def checkCanMove(self, dx, dy):
        if not self.position.level or \
            not self.position.level.map.checkInBounds(dx, dy) or \
            not self.position.level.map.checkIsPassable(dx, dy) or \
            self.position.level.map.checkIsBlocked(dx, dy):
            return False
        return True



class GetTargetAction(EntityAction):
    def __init__(self, entity, targetRange, targetType="NPC"):
        super().__init__(entity)
        self.targetType = targetType
        self.targetRange = targetRange

    def perform(self):
        targets = []
        currentTargetIndex = -1

        for entity in self.entity.world.create_query(all_of=[self.targetType]).result:
            if entity["Position"].level.map.checkIsVisible(entity):
                targetRange = max(abs(self.entity.x - entity.x), abs(self.entity.y - entity.y))
                targets.append((entity, targetRange))

        targets.sort(key = lambda x: x[1])
        
        counter = 0
        for entity in targets:
            if entity[0] == self.entity["Target"].target:
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

            
            self.entity.fire_event("clear_target")

            finalTarget = targets[currentTargetIndex][0]
            self.entity.fire_event("set_target", {"target": finalTarget})
            finalTarget.fire_event("add_targeter", {"entity": self.entity})

        else:
            if self.entity.target:
                self.entity.target.targettedBy.remove(self.entity)
            self.entity.target = None

        print (f"Player {self.entity}\nis now targetting {self.entity['Target'].target}\nfrom list {targets}")
