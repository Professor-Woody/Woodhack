from Systems.BaseSystem import BaseSystem
from Actions.MoveActions import MovementAction
from Components.FlagComponents import IsReady

class MoveSystem(BaseSystem):
    def run(self):
        # print ("move start")
        for action in self.actionQueue:
            print (action)
            if type(action) == MovementAction:
                self.move(action)
        self.actionQueue.clear()
        # print ("move end")

    
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
            if action.entity.has(IsReady):
                action.entity.remove(IsReady)

    def checkCanMove(self, dx, dy):
        if not self.level.map.checkInBounds(dx, dy) or \
            not self.level.map.checkIsPassable(dx, dy) or \
            self.level.map.checkIsBlocked(dx, dy):
            return False
        return True