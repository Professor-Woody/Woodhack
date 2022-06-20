from Systems.BaseSystem import BaseSystem


class MoveSystem(BaseSystem):
    def run(self):
        for action in self.actionQueue:
            if type(action) == MovementAction:
                self.move(action)

    
    def move(self, action):
        position = action.position
        dx = action.dx
        dy = action.dy
        speed = action.speed
        initiative = action.initiative

        newLocationX = position.x + dx
        newLocationY = position.y + dy

        if self.checkCanMove(newLocationX, newLocationY):
            pass
        else:
            if not self.checkCanMove(newLocationX, position.y):
                dx = 0
            if not self.checkCanMove(position.x + dx, newLocationY):
                dy = 0

        if dx or dy:
            position.x += dx
            position.y += dy
            initiative.speed += speed

    def checkCanMove(self, dx, dy):
        if not self.level.map.checkInBounds(dx, dy) or \
            not self.level.map.checkIsPassable(dx, dy) or \
            self.level.map.checkIsBlocked(dx, dy):
            return False
        return True