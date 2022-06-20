from Actions.BaseActions import EntityAction

class MoveAction(EntityAction):
    pass


class MovementAction(MoveAction):
    def __init__(self, entity, position, dx, dy, speed):
        super().__init__(entity)
        self.position = position
        self.dx = dx
        self.dy = dy
        self.speed = speed