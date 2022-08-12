

class RectangularRoom:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x2 = x + width
        self.y2 = y + height


    @property
    def center(self):
        """return centre of room"""
        centerX = int((self.x + self.x2) / 2)
        centerY = int((self.y + self.y2) / 2)

        return centerX, centerY
    
    @property
    def inner(self):
        """return inner area as a 2d array index"""
        return slice(self.x + 1, self.x2), slice(self.y + 1, self.y2)

    def intersects(self, other):
        return (
            self.x <= other.x2
            and self.x2 >= other.x
            and self.y < other.y2
            and self.y2 >= other.y
        )