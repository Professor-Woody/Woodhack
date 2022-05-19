
class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = np.full((self.width, self.height), fill_value=wall, order="F")
        self.visible = np.full((self.width, self.height), fill_value=False, order="F")
        self.explored = np.full((self.width, self.height), fill_value=False, order="F")

        self.start = None
        self.end = None


    def checkIsPassable(self, x, y):
        return self.tiles["passable"][x, y]


    def checkInBounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def checkIsVisible(self, entity):
        return self.visible[entity.x, entity.y]


    def update(self, players):
        # update FOV
        for player in players:
            self.visible[:] = compute_fov(
                self.tiles["transparent"],
                (player.x, player.y),
                radius=5,
                algorithm=tcod.FOV_SYMMETRIC_SHADOWCAST
            )
        self.explored |= self.visible


    def draw(self, screen):
        screen.drawArray(
            (0,self.width), 
            (0,self.height),
            np.select(
                condlist=[self.visible, self.explored],
                choicelist=[self.tiles["light"], self.tiles["dark"]],
                default=SHROUD
                )
        )

