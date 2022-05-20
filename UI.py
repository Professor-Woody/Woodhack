import Colours as colour

def renderHPBar(screen, x, y, value, maxValue, totalWidth):
    barWidth = int(float(value) / maxValue * totalWidth)
    
    screen.drawRect(x, y, totalWidth, 1, 1, colour.BAR_EMPTY)

    if barWidth > 0:
        screen.drawRect(x, y, barWidth, 1, 1, colour.BAR_FILLED)

    screen.print(x+1, y, f"HP: {value}/{maxValue}", colour.BAR_TEXT)