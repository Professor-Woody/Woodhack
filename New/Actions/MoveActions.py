from Actions.BaseActions import MoveAction
from Components.Components import Position, Initiative

class MovementAction(MoveAction):
    def __init__(self, entity, dx, dy, speed):
        super().__init__(entity)
        self.position = entity[Position]
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.initiative = entity[Initiative]