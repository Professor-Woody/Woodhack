from select import select
from Components import *
from Systems.BaseSystem import BaseSystem
import Colours as colour

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
                if inputComponents[selectionComponents[entity]['parentEntity']]['controller'].getPressedOnce('up'):
                    selectionComponents[entity]['selectionIndex'] -= 1 
                    if selectionComponents[entity]['selectionIndex'] < 0:
                        selectionComponents[entity]['selectionIndex'] = len(selectionComponents[entity]['items']) - 1
                        print (f"setting index to {selectionComponents[entity]['selectionIndex']}")
                
                elif inputComponents[selectionComponents[entity]['parentEntity']]['controller'].getPressedOnce('down'):
                    selectionComponents[entity]['selectionIndex'] += 1 
                    if selectionComponents[entity]['selectionIndex'] >= len(selectionComponents[entity]['items']):
                        selectionComponents[entity]['selectionIndex'] = 0            
                        print (f"setting index to {selectionComponents[entity]['selectionIndex']}")

                for command, result in selectionComponents[entity]['commands'].items():
                    if inputComponents[selectionComponents[entity]['parentEntity']]['controller'].getPressedOnce(command):
                        if 'data' in result.keys():
                            data = result['data']
                        else:
                            data = {}
                        data['ui'] = entity
                        data['entity'] = selectionComponents[entity]['parentEntity']
                        data['items'] = selectionComponents[entity]['items']
                        data['item'] = selectionComponents[entity]['items'][selectionComponents[entity]['selectionIndex']]  if  selectionComponents[entity]['items'] else None

                        self.level.post(result['action'], data)


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
            equippedComponents = self.getComponents(Equipped)

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
                    title = renderComponents[selectionComponents[entity]['items'][i]]['name']
                    if selectionComponents[entity]['items'][i] in equippedComponents.keys():
                        title += " - " + equippedComponents[selectionComponents[entity]['items'][i]]['slot']
                    screen.printLine(
                        positionComponents[entity]['x']+2,
                        positionComponents[entity]['y']+1+i,
                        title,
                        renderComponents[selectionComponents[entity]['items'][i]]['fg'],
                        colour.GREY if selectionComponents[entity]['selectionIndex'] == i else None
                    )     


