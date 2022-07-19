from select import select
from Components import *
from Systems.BaseSystem import BaseSystem

class RenderEntitiesSystem(BaseSystem):
    def run(self):
        entities = self.level.renderQuery.result
        renderComponents = self.level.e.component.filter(Render, entities)
        positionComponents = self.level.e.component.filter(Position, entities)
        screen = self.level.app.screen

        for entity in entities:
            if (renderComponents[entity]['needsVisibility'] and self.level.map.checkIsVisible(positionComponents[entity]['x'], positionComponents[entity]['y'])) \
            or not renderComponents[entity]['needsVisibility']:
                screen.draw(
                    positionComponents[entity]['x'], 
                    positionComponents[entity]['y'],
                    renderComponents[entity]['char'],
                    renderComponents[entity]['fg'],
                    renderComponents[entity]['bg'])
            

class UpdateSelectionUISystem(BaseSystem):
    def run(self):
        entities = self.level.selectionUIQuery.result
        if entities:
            selectionComponents = self.getComponents(SelectionUI)
            inputComponents = self.getComponents(PlayerInput)
            
            for entity in entities:
                for command, result in selectionComponents[entity]['commands'].items():
                    if inputComponents[selectionComponents[entity]['parentEntity']]['controller'].getPressedOnce(command):
                        self.level.post(result['action'], {
                            'ui': entity,
                            'entity': selectionComponents[entity]['parentEntity'],
                            'items': selectionComponents[entity]['items'],
                            'item': selectionComponents[entity]['items'][selectionComponents[entity]['selectionIndex']]  if  selectionComponents[entity]['items'] else None
                        })

class CloseUISystem(BaseSystem):
    actions=['close_selection']

    def run(self):
        if self._actionQueue:
            inputComponents = self.getComponents(PlayerInput)

            for action in self.actionQueue:
                self.level.e.destroyEntity(action['ui'])
                inputComponents[action['entity']]['controlFocus'].remove(action['ui'])
            


class RenderSelectionUISystem(BaseSystem):
    def run(self):
        entities = self.level.selectionUIQuery.result
        if entities:
            screen = self.level.app.screen
            selectionComponents = self.getComponents(SelectionUI)
            renderComponents = self.getComponents(Render)
            positionComponents = self.getComponents(Position)

            for entity in entities:
                # draw the frame
                screen.drawFrame(
                    positionComponents[entity]['x'],
                    positionComponents[entity]['y'],
                    positionComponents[entity]['width'],
                    positionComponents[entity]['height'],
                    selectionComponents[entity]['title']
                    )

                # draw the list of items
                for i in range(len(selectionComponents[entity]['items'])):
                    screen.printLine(
                        positionComponents[entity]['x']+2,
                        positionComponents[entity]['y']+1+i,
                        renderComponents[selectionComponents[entity]['items'][i]]['name'],
                        renderComponents[selectionComponents[entity]['items'][i]]['fg']
                    )     




                # check the inputs and perform actions
