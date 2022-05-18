import tcod

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        tileset = tcod.tileset.load_tilesheet(
                "dejavu10x10_gs_tc.png",
                32,
                8,
                tcod.tileset.CHARMAP_TCOD
            )

        self.context = tcod.context.new_terminal(self.width, self.height, tileset=tileset, title="blah", vsync=True)
        self.console = tcod.Console(self.width, self.height, order="F")

    def clear(self):
        self.console.clear()

    def draw(self, entity):
        self.console.print(x=entity.x, y=entity.y, string=entity.char)
    
    def drawArray(self, horizontal, vertical, array):
        self.console.tiles_rgb[horizontal[0]:horizontal[1], vertical[0]:vertical[1]] = array

    def flip(self):
        self.context.present(self.console)


