class Component:
    def __init__(self, parent):
        self.parent = parent
    
    def act(self):
        pass

class PositionBoxComponent(Component):
    def areaCollides(self, other):
        return False
    
    def pointCollides(self, x, y):
        return False


class CollisionBoxComponent(PositionBoxComponent):
    def areaCollides(self, other):
        return (
            self.parent.x < other.x+other.width
            and self.parent.x+self.parent.width >= other.x
            and self.parent.y < other.y+other.height
            and self.parent.y+self.parent.height >= other.y
        )
    
    def pointCollides(self, x, y):
        return (
            x >= self.parent.x
            and x < self.parent.x + self.parent.width
            and y >= self.parent.y
            and y < self.parent.y + self.parent.height
        )
