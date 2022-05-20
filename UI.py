import Colours as colour

def renderHPBar(screen, value, maxValue, totalWidth):
    barWidth = int(float(value) / maxValue * totalWidth)
    
    screen.drawRect(0, 45, totalWidth, 1, 1, colour.BAR_EMPTY)

    if barWidth > 0:
        screen.drawRect(0, 45, width, 1, 1, colour.BAR_FILLED)

    screen.print(1, 45, f"HP: {value}/{maxValue}", colour.BAR_TEXT)