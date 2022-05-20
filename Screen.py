import tcod
import Colours as colour

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

    def drawRect(self, x, y, width, height, ch, background):
        self.console.draw_rect(x=x, y=y, width=width, height=height, ch=ch, bg=background)
    
    def drawArray(self, horizontal, vertical, array):
        self.console.rgb[horizontal[0]:horizontal[1], vertical[0]:vertical[1]] = array

    def print(self, x, y, msg, foreground = colour.WHITE):
        self.console.print(x=x, y=y, string=msg, fg=foreground)

    def flip(self):
        self.context.present(self.console)


