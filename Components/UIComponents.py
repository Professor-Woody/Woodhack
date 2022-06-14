from ecstremity import Component
from Components.Components import Position
from Actions.UIActions import GetSelectionInputAction

class UI(Component):
    pass

class SelectionUI(Component):
    def __init__(self, parentEntity, items, actions):
        self.parentEntity = parentEntity
        self.items = items
        self.choice = 0
        self.actions = actions

    def on_update(self, event):
        event.data.actions.append(GetSelectionInputAction(self.entity))

    def on_draw(self, event):
        screen = event.data.screen
        screen.drawFrame(
            self.entity[Position].x,
            self.entity[Position].y,
            self.entity[Position].width,
            self.entity[Position].height,
            "Pick up:"
        )
        for i in range(min(len(self.entity['SelectionUI'].items), 10)):
            if i == self.choice:
                screen.printLine(self.entity[Position].x+2, self.entity[Position].y+i+1, self.entity['SelectionUI'].items[i][Render].entityName, fg=colour.BLACK, bg=colour.WHITE)
            else:
                screen.printLine(self.entity[Position].x+2, self.entity[Position].y+i+1, self.entity['SelectionUI'].items[i][Render].entityName)
