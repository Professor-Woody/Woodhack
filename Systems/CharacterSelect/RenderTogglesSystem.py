from Components import Position, Render, Selected, ToggleUI
from Systems.BaseSystem import BaseSystem
import Colours as colour


class RenderTogglesSystem(BaseSystem):

    def run(self):
        entities = self.level.togglesQuery.result
        toggleComponents = self.getComponents(ToggleUI)
        renderComponents = self.getComponents(Render)
        positionComponents = self.getComponents(Position)
        screen = self.level.app.screen

        for entity in entities:
            bg = colour.BLACK
            if self.level.e.hasComponent(entity, Selected):
                bg = colour.GREY

            screen.printLine(
                positionComponents[entity]['x'],
                positionComponents[entity]['y'],
                renderComponents[entity]['name'],
                bg=bg
            )
            if toggleComponents[entity]['displaySelection']:
                screen.printLine(
                    positionComponents[entity]['x'],
                    positionComponents[entity]['y']+1,
                    str(toggleComponents[entity]['selection'][toggleComponents[entity]['index']]),
                )

                