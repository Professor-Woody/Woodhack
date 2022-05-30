from Actions import Action


class EntityAction(Action):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity



class MovementAction(EntityAction):
    def __init__(self, entity, x, y):
        super().__init__(entity)
        self.x = x
        self.y = y

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