import Colours as colour
import Entity
import Colours as colour


def renderHPBar(screen, x, y, value, maxValue, totalWidth):
    barWidth = int(float(value) / maxValue * totalWidth)
    
    screen.drawRect(x, y, totalWidth, 1, 1, colour.BAR_EMPTY)

    if barWidth > 0:
        screen.drawRect(x, y, barWidth, 1, 1, colour.BAR_FILLED)

    screen.print(x+1, y, f"HP: {value}/{maxValue}", colour.BAR_TEXT)


class CollisionBox:
    x=0
    y=0
    width=0
    height=0

    def areaCollides(self, other):
        return (
            self.x < other.x+other.width
            and self.x+self.width >= other.x
            and self.y < other.y+other.height
            and self.y+self.height >= other.y
        )
    
    def pointCollides(self, x, y):
        return (
            x >= self.x
            and x < self.x + self.width
            and y >= self.y
            and y < self.y + self.height
        )

class Button(Entity, CollisionBox):
    def __init__(self, level, x, y, width, height, msg, action=None):
        Entity.__init__(self, "UI", "B", colour.GREY)
        CollisionBox.__init__(self)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.msg = msg

        self.changed = False
        self.selected = False
        self.pressed = False
        self.bg = colour.GREY
        self.fg = colour.WHITE

        self.action = action(self)

    def update(self):
        # if selected then highlight
        if self.changed:
            self.changed = False
            if self.selected and not self.pressed:
                self.bg = colour.LIGHT_GREY
                self.fg = colour.BLACK
            else:
                self.bg = colour.GREY
                self.fg = colour.WHITE

    def draw(self, screen):
        screen.drawFrame(self.x, self.y, self.width, self.height, msg=self.msg, bg=self.bg, fg=self.fg)




STARTED = 0
OPENING = 1
OPENED = 2
CLOSING = 3

class TextBox:
    def __init__(self, x, y, msg, title="", timeToLive=-1, width=0, height=0):
        self.x = x
        self.y = y
        self.state = OPENING
        self.timeToLive = timeToLive

        self.msg = msg
        self.title = title

        self.width = width
        self.height = height
        self.currentWidth = self.width
        self.currentHeight = self.height

        if not self.width and not self.height:
            maxLength = 0
            lines = 1
            msg = msg.split("\n")
            for line in msg:
                if len(line) > maxLength:
                    maxLength = len(line)
                lines += 1
            self.width = 8 + maxLength

            self.height = 2 + lines

        self.speed = 2
        self.update()

        self.state = OPENING



    def update(self):
        if self.state == OPENING:            
            if self.speed:
                self.speed -= 1
                return
            self.speed = 2
            
            if (self.currentHeight == self.height and self.currentWidth == self.width):
                self.state = OPENED

            self.currentWidth += max(min(self.width-self.currentWidth, 1), -1)
            self.currentHeight += max(min(self.height-self.currentHeight, 1), -1)

            if self.currentHeight == self.height and self.currentWidth == self.width:          
                self.state == OPENED

        elif self.state == OPENED:
            if self.timeToLive == -1:
                pass
            elif self.timeToLive > 0:
                self.timeToLive -= 1
            else:
                self.state = CLOSING


    def updateText(self, msg):
        self.msg
        maxLength = 0
        msg = msg.split("\n")
        lines = 1
        for line in msg:
            lines += 1
            if len(line) > maxLength:
                maxLength = len(line)

        self.width = 2 + maxLength       
        self.height = 2 + lines        
        self.state = OPENING


    def draw(self, screen):
        if self.state == OPENING:
            screen.drawFrame(self.x, self.y, self.currentWidth, self.currentHeight)
        if self.state == OPENED:
            screen.drawFrame(self.x, self.y, self.currentWidth, self.currentHeight, f"┤{self.title}├", self.msg)


