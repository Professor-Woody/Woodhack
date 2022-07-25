from Components import ButtonUI, Position, Render
from Systems.BaseSystem import BaseSystem
from Controllers import controllers
import Colours as colour
import copy

class UpdateButtonsSystem(BaseSystem):
    selectionIndex = 0



    def run(self):
        entities = self.level.buttonsQuery.result
        uiComponents = self.getComponents(ButtonUI)
        

        # check if any of the controllers have pressed up or down
            # select button based on movement
        changed = False
        pressed = False

        for controller in controllers:
            controller.update()

            if controller.getPressedOnce('up'):
                self.selectionIndex -= 1
                if self.selectionIndex < 0:
                    self.selectionIndex = len(entities) - 1
                changed = True

            if controller.getPressedOnce('down'):
                self.selectionIndex += 1
                if self.selectionIndex >= len(entities):
                    self.selectionIndex = 0
                changed = True

            if controller.getPressedOnce("use"):
                pressed = True

        if changed:
            for entity in entities:
                uiComponents[entity]['selected'] = False
            uiComponents[entities[self.selectionIndex]]['selected'] = True
        
        if pressed:
            self.level.post(uiComponents[entities[self.selectionIndex]]['action'], copy.deepcopy(uiComponents[entities[self.selectionIndex]]['data']))
                
    
        # check if any of the controllers have pressed use
            # trigger button action for actively selected button


class RenderButtonsSystem(BaseSystem):

    def run(self):
        entities = self.level.buttonsQuery.result
        positionComponents = self.getComponents(Position)
        uiComponents = self.getComponents(ButtonUI)
        renderComponents = self.getComponents(Render)

        screen = self.level.app.screen

        for entity in entities:
            bg = colour.BLACK
            fg = colour.WHITE
            if uiComponents[entity]['selected']:
                bg = colour.GREY
                fg = colour.WHITE

            screen.drawFrame(
                positionComponents[entity]['x'],
                positionComponents[entity]['y'],
                positionComponents[entity]['width'],
                positionComponents[entity]['height'],
                fg=fg,
                bg=bg
            )

            centerx = positionComponents[entity]['x'] + int(positionComponents[entity]['width']/ 2)
            centery = positionComponents[entity]['y'] + int(positionComponents[entity]['height']/ 2)

            screen.printLine(
                centerx - int(len(renderComponents[entity]['name'])/2),
                centery,
                renderComponents[entity]['name'],
                fg=fg,
                bg=bg
            )
