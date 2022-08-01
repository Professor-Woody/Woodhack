from Systems.BaseSystem import BaseSystem
from Components import *

class MoveSystem(BaseSystem):
    actions=['move']
    alwaysActive=False
    priority=120
    
    def run(self):
        print ("-----Moving-----")
        positionComponents = self.level.e.component.components[Position]

        for action in self.actionQueue:
            newx = positionComponents[action['entity']]['x'] + action['dx']
            newy = positionComponents[action['entity']]['y'] + action['dy']

            if not self.checkCanMove(newx, newy):
                dx = 0
                dy = 0
                if self.checkCanMove(newx, positionComponents[action['entity']]['y']):
                    dx = action['dx']
                elif self.checkCanMove(positionComponents[action['entity']]['x'], newy):
                    dy = action['dy']
                action['dx'] = dx
                action['dy'] = dy

            if action['dx'] or action['dy']:
                positionComponents[action['entity']]['x'] += action['dx']
                positionComponents[action['entity']]['y'] += action['dy']


    def checkCanMove(self, x, y):
        if not self.level.map.checkInBounds(x, y) or \
            not self.level.map.checkIsPassable(x, y) or \
            self.level.map.checkIsBlocked(x, y):
            return False
        return True