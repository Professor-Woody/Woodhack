class Component:
    def __init__(self, entity):
        self.entity = entity
    
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
            self.entity.x < other.x+other.width
            and self.entity.x+self.entity.width >= other.x
            and self.entity.y < other.y+other.height
            and self.entity.y+self.entity.height >= other.y
        )
    
    def pointCollides(self, x, y):
        return (
            x >= self.entity.x
            and x < self.entity.x + self.entity.width
            and y >= self.entity.y
            and y < self.entity.y + self.entity.height
        )

