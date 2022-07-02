import tcod
import Colours as colour
from Components.Components import Position, Render

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
        self.console.print(x=entity[Position].x, y=entity[Position].y, string=entity[Render].char, fg=entity[Render].fg, bg=entity[Render].bg)

    def drawRect(self, x, y, width, height, ch, background):
        self.console.draw_rect(x=x, y=y, width=width, height=height, ch=ch, bg=background)
    
    def drawArray(self, horizontal, vertical, array):
        self.console.rgb[horizontal[0]:horizontal[1], vertical[0]:vertical[1]] = array

    def drawFrame(self, x, y, width, height, title="", msg="", bg=None, fg=colour.WHITE):
        self.console.draw_frame(x, y, width, height, clear=True, fg=fg, bg=bg)
        self.console.print_box(x, y, width, height, string=title, bg=bg, alignment=tcod.constants.CENTER)
        self.console.print_box(x+1, y+1, width-1, height-1, msg, bg=bg)

    def print(self, x, y, msg, fg = colour.WHITE):
        self.console.print(x=x, y=y, string=msg, fg=fg)

    def printLine(self, x, y, msg, fg=colour.WHITE, bg=colour.BLACK):
        self.console.print_box(x, y, width=len(msg), height=1, string=msg, fg=fg, bg=bg)
            
    def printLines(self, x, y, msg, fg=colour.WHITE, bg=colour.BLACK):
        width = 0
        lines = msg.split("\n")
        for line in lines:
            width = max(width, len(line))
        height = len(lines)
        self.console.print_box(x, y, width, height, msg, fg=fg, bg=bg)
        

    def flip(self):
        self.context.present(self.console)

