from Systems.BaseSystem import BaseSystem
from Components import *

class MoveSystem(BaseSystem):
    actions=['move']
    def run(self):
        positionComponents = self.level.e.component.components[Position]

        for action in self.actionQueue:
            newx = positionComponents[action['entity']]['x'] + action['dx']
            newy = positionComponents[action['entity']]['y'] + action['dy']
            if not self.checkCanMove(newx, newy):
                if not self.checkCanMove(newx, positionComponents[action['entity']]['y']):
                    action['dx'] = 0
                elif not self.checkCanMove(positionComponents[action['entity']]['x'], newy):
                    action['dy'] = 0
            if action['dx'] or action['dy']:
                positionComponents[action['entity']]['x'] += action['dx']
                positionComponents[action['entity']]['y'] += action['dy']


    def checkCanMove(self, x, y):
        if not self.level.map.checkInBounds(x, y) or \
            not self.level.map.checkIsPassable(x, y) or \
            self.level.map.checkIsBlocked(x, y):
            return False
        return True