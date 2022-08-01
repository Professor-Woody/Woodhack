from Components import Position, Stat
from Systems.BaseSystem import BaseSystem


class RenderStatDisplaySystem(BaseSystem):
    priority=100

    def run(self):
        entities = self.level.statDisplayQuery.result
        statComponents = self.getComponents(Stat)
        positionComponents = self.getComponents(Position)
        screen = self.level.app.screen

        for entity in entities:
            # display value?
            screen.printLine(
                positionComponents[entity]['x'],
                positionComponents[entity]['y'],
                str(statComponents[entity]['value'])
            )
