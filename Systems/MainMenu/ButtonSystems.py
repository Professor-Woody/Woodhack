from Components import ButtonUI, Position, Render, Selected, SliderUI
from Systems.BaseSystem import BaseSystem
from Controllers import controllers
import Colours as colour
import copy

class UpdateButtonsSystem(BaseSystem):
    selectionIndex = 0



    def run(self):
        entities = self.level.uiInputsQuery.result
        buttonComponents = self.getComponents(ButtonUI) 
        sliderComponents = self.getComponents(SliderUI)
        

        # check if any of the controllers have pressed up or down
            # select button based on movement
        changed = False
        pressed = False
        toggleValue = 0

        for controller in controllers:
            controller.update()

            if controller.getPressedOnce('up'):
                self.selectionIndex -= 1
                if self.selectionIndex < 0:
                    self.selectionIndex = len(entities) - 1
                changed = True

            elif controller.getPressedOnce('down'):
                self.selectionIndex += 1
                if self.selectionIndex >= len(entities):
                    self.selectionIndex = 0
                changed = True

            if controller.getPressedOnce("left"):
                toggleValue = -1
            elif controller.getPressedOnce("right"):
                toggleValue = 1

            if controller.getPressedOnce("use"):
                pressed = True

        if changed:
            for entity in entities:
                if self.level.e.hasComponent(entity, Selected):
                    self.level.e.removeComponent(entity, Selected)

            self.level.e.addComponent(entities[self.selectionIndex], Selected)

        if toggleValue:
            if self.level.e.hasComponent(entities[self.selectionIndex], SliderUI):
                sliderComponents[entities[self.selectionIndex]]['value'] += toggleValue
                if sliderComponents[entities[self.selectionIndex]]['value'] < 0:
                    sliderComponents[entities[self.selectionIndex]]['value'] = 0
                elif sliderComponents[entities[self.selectionIndex]]['value'] > 10:
                    sliderComponents[entities[self.selectionIndex]]['value'] = 10

        if pressed:
            if self.level.e.hasComponent(entities[self.selectionIndex], ButtonUI):
                self.level.post(buttonComponents[entities[self.selectionIndex]]['action'], copy.deepcopy(buttonComponents[entities[self.selectionIndex]]['data']))
                
    
        # check if any of the controllers have pressed use
            # trigger button action for actively selected button


class RenderButtonsSystem(BaseSystem):

    def run(self):
        # Buttons
        entities = self.level.buttonsQuery.result
        positionComponents = self.getComponents(Position)
        uiComponents = self.getComponents(ButtonUI)
        renderComponents = self.getComponents(Render)

        screen = self.level.app.screen

        for entity in entities:
            bg = colour.BLACK
            fg = colour.WHITE
            if self.level.e.hasComponent(entity, Selected):
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

            screen.printLines(
                positionComponents[entity]['x']+2,
                positionComponents[entity]['y']+1,
                renderComponents[entity]['name'],
                fg=fg,
                bg=bg
            )

class RenderSlidersSystem(BaseSystem):

    def run(self):
        # sliders
        entities = self.level.slidersQuery.result

        positionComponents = self.getComponents(Position)
        sliderComponents = self.getComponents(SliderUI)
        renderComponents = self.getComponents(Render)

        screen = self.level.app.screen

        for entity in entities:
            screen.printLine(
                positionComponents[entity]['x'],
                positionComponents[entity]['y'],
                renderComponents[entity]['name']
            )
            screen.printLine(
                positionComponents[entity]['x'],
                positionComponents[entity]['y']+1,
                f"I---------I  {sliderComponents[entity]['value'] * 10}%  ",
                fg=colour.LIGHT_ORANGE,
                bg=colour.GREY if self.level.e.hasComponent(entity, Selected) else colour.BLACK
            )
            screen.printLine(
                positionComponents[entity]['x'] + sliderComponents[entity]['value'],
                positionComponents[entity]['y']+1,
                "O",
                fg=colour.GREEN,
                bg=colour.GREY if self.level.e.hasComponent(entity, Selected) else colour.BLACK
            )
            


