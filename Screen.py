import tcod
import Colours as colour

styles = {
    'single': "┌─┐│ │└─┘",
    'double': "╔═╗║ ║╚═╝",
    'left': "╓─┐║ │╙─┘",
    'top': '╒═╕│ │└─┘',
    'topleft': '╔═╕║ │╙─┘',
    'bottomright': '┌─╖│ ║╘═╝',
    'topleftopen': '╔═╕║  ╙  ',
    'speckles': '░░░░ ░░░░',
    'solid': '████ ████',
    'open': '         ',
    'frame': "╔─╗│ │╚─╝"
}
styleSides = {
    'single': '┤├',
    'double': '╡╞',
    'left': '┤├',
    'top': '╡╞',
    'topleft': '╡╞',
    'bottomright': '┤├',
    'topleftopen': '╡╞',
    'speckles': '░░',
    'solid': '██',
    'open': '  ',
    'frame': '┤├',
}

class Screen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # tcod.lib.SDL_SetHint(b"SDL_RENDER_SCALE_QUALITY", b"0")
        tileset = tcod.tileset.load_tilesheet(
                # "tilesets/dejavu10x10_gs_tc.png",
                # "tilesets/Cheepicus_12x12.png",
                # "tilesets/yayo_10x10.png",
                "tilesets/Pastiche_8x8.png",
                # "tilesets/Taffer_10x10.png",
                # "tilesets/dejavu8x8_gs_tc.png",
                # "tilesets/dejavu16x16_gs_tc.png",
                # 32,8,
                16,16,
                tcod.tileset.CHARMAP_CP437
                # tcod.tileset.CHARMAP_TCOD
            )
        
        self.context = tcod.context.new_terminal(self.width, self.height, tileset=tileset, title="I need a title", vsync=True)
        self.console = tcod.Console(self.width, self.height, order="F")

    def clear(self):
        self.console.clear()

    def draw(self, x, y, char, fg=colour.WHITE, bg=None):
        self.console.print(
            x=x, 
            y=y, 
            string=char, 
            fg=fg, 
            bg=bg)
    
    def drawRect(self, x, y, width, height, ch, background):
        self.console.draw_rect(x=x, y=y, width=width, height=height, ch=ch, bg=background)
    
    def drawArray(self, horizontal, vertical, array):
        self.console.rgb[horizontal[0]:horizontal[1], vertical[0]:vertical[1]] = array

    def drawFrame(self, x, y, width, height, title="", msg="", bg=None, fg=colour.WHITE, style='frame'):
        self.console.draw_frame(x, y, width, height, clear=True, fg=fg, bg=bg, decoration=styles[style] ) #decoration=(201, 205, 187, 186, 32, 186, 200,205, 188))
        if title:
            self.console.print_box(x+2, y, width, height, string= f"{styleSides[style][0]}{title}{styleSides[style][1]}", bg=bg)#, alignment=tcod.constants.CENTER)
        if msg:
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


