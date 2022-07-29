from Components import IsPlayer, Position, Render, StatPoints
from Systems.BaseSystem import BaseSystem
import Colours as colour

class RenderCharacterPanesSystem(BaseSystem):

    def run(self):
        screen = self.level.app.screen
        positionComponents = self.getComponents(Position)
        playerComponents = self.getComponents(IsPlayer)
        renderComponents = self.getComponents(Render)

        entities = self.level.unclaimedPanesQuery.result
        for entity in entities:
            screen.drawFrame(
                positionComponents[entity]['x'],
                positionComponents[entity]['y'],
                positionComponents[entity]['width'],
                positionComponents[entity]['height'],
                f" Player {playerComponents[entity]['id']+1} ",
                fg=renderComponents[entity]['fg'],
                bg=colour.BLACK
            )
            screen.printLines(
                positionComponents[entity]['x']+2,
                positionComponents[entity]['y']+2,
                "Press \nTo Join")
            screen.printLine(
                positionComponents[entity]['x']+8,
                positionComponents[entity]['y']+2,
                "'Use'",
                fg=colour.GREEN
            )

        entities = self.level.claimedPanesQuery.result
        pointsComponents = self.getComponents(StatPoints)

        for entity in entities:
            screen.drawFrame(
                positionComponents[entity]['x'],
                positionComponents[entity]['y'],
                positionComponents[entity]['width'],
                positionComponents[entity]['height'],
                f" Player {playerComponents[entity]['id']+1} ",
                fg=renderComponents[entity]['fg'],
                bg=colour.BLACK
            )
            screen.printLine(
                positionComponents[entity]['x']+2,
                positionComponents[entity]['y']+6,
                f"Points: {pointsComponents[entity]['value']}"
            )

