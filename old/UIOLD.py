import Colours as colour
import tcod
import numpy as np

def renderHPBar(screen, x, y, value, maxValue, totalWidth):
    barWidth = int(float(value) / maxValue * totalWidth)
    
    screen.drawRect(x, y, totalWidth, 1, 1, colour.BAR_EMPTY)

    if barWidth > 0:
        screen.drawRect(x, y, barWidth, 1, 1, colour.BAR_FILLED)

    screen.print(x+1, y, f"HP: {value}/{maxValue}", colour.BAR_TEXT)


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

        self.msg = msg.split("\n")
        self.title = title

        self.width = width
        self.height = height
        self.currentWidth = self.width
        self.currentHeight = self.height

        if not self.width and not self.height:
            maxLength = 0
            for line in self.msg:
                if len(line) > maxLength:
                    maxLength = len(line)
            self.width = 2 + maxLength

            lines = 1 + len(self.msg)
            self.height = 2 + lines

        self.update()

        self.state = OPENING


    def update(self):
        if self.state == OPENING:
            print ("opening")
            if (self.currentHeight == self.height and self.currentWidth == self.width):
                self.state = OPENED

            self.currentWidth += max(min(self.width-self.currentWidth, 1), -1)
            self.currentHeight += max(min(self.height-self.currentHeight, 1), -1)

            self.buffer = np.full(
                shape=(self.currentWidth, self.currentHeight),
                fill_value=ord(' '),
                dtype=tcod.console.Console.DTYPE,
                order="F"
            )
            self.buffer["ch"][:,0] = ord('-')
            self.buffer["ch"][:,self.currentHeight-1] = ord('-')
            self.buffer["ch"][0,:]=ord('|')
            self.buffer["ch"][self.currentWidth-1,:]=ord('|')

            if self.currentHeight == self.height and self.currentWidth == self.width:
                row = 1
                for line in self.msg:
                    cursor = 1
                    for letter in line:
                        self.buffer["ch"][cursor,row]=ord(letter)
                        cursor += 1
                    row += 1                
                self.state == OPENED

        elif self.state == OPENED:
            if self.timeToLive == -1:
                pass
            elif self.timeToLive > 0:
                self.timeToLive -= 1
            else:
                self.state = CLOSING


    def updateText(self, msg):
        self.msg = msg
        maxLength = 0
        for line in self.msg:
            if len(line) > maxLength:
                maxLength = len(line)
        self.width = 2 + maxLength

        lines = 1 + len(self.msg)
        self.height = 2 + lines        
        self.state = OPENING


    def draw(self, screen):
        screen.drawArray(
            (self.x, self.x+self.currentWidth),
            (self.y, self.y+self.currentHeight),
            self.buffer
        )


