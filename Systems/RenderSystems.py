from select import select
from Components import *
from Screen import Screen
from Systems.BaseSystem import BaseSystem
import Colours as colour

class RenderEntitiesSystem(BaseSystem):
    def run(self):
        entities = self.level.itemsOnGroundQuery.result + self.level.npcsQuery.result + self.level.playersQuery.result
        # renderComponents = self.level.e.component.filter(Render, entities)
        # positionComponents = self.level.e.component.filter(Position, entities)
        renderComponents = self.getComponents(Render)
        positionComponents = self.getComponents(Position)
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
            

class RenderPlayerUISystem(BaseSystem):
    def run(self):
        entities = self.level.playersQuery.result
        bodyComponents = self.getComponents(Body)
        statsComponents = self.getComponents(Stats)
        renderComponents = self.getComponents(Render)
        idComponents = self.getComponents(IsPlayer)
        initComponents = self.getComponents(Init)
        targetComponents = self.getComponents(Target)
        screen: Screen = self.level.app.screen

        for entity in entities:
            # draw the frame
            y = idComponents[entity]['id'] * 16

            screen.drawFrame(
                self.level.width - 24,
                y,
                24,
                16,
                renderComponents[entity]['name'],
                fg=renderComponents[entity]['fg'],
                bg = colour.BLACK
            )

            # draw info:
                # equipment/ready state
                # cooldown state
                # health
                # conditions
                # target
                # target health

            # --------
            # mainhand
            if bodyComponents[entity]['mainhand']:
                screen.printLine(self.level.width - 12, y + 2, renderComponents[bodyComponents[entity]['mainhand']]['name'], renderComponents[bodyComponents[entity]['mainhand']]['fg'], bg=None)
                
                if self.level.e.hasComponent(bodyComponents[entity]['mainhand'], Init):
                    # if not initComponents[bodyComponents[entity]['mainhand']]['speed']:
                        # screen.draw(self.level.width - 24, y + 2, 'o', colour.GREEN)
                    # else:
                        # screen.draw(self.level.width - 24, y + 2, 'o', colour.RED)
                    if initComponents[bodyComponents[entity]['mainhand']]['speed']:
                        # screen.printLine(self.level.width - 22, y + 2, " " * int(20 * (initComponents[bodyComponents[entity]['mainhand']]['speed']/initComponents[bodyComponents[entity]['mainhand']]['maxSpeed'])), fg=colour.RED, bg=colour.RED)
                        # screen.printLine(self.level.width - 17, y + 2, f"{initComponents[bodyComponents[entity]['mainhand']]['speed']} / {initComponents[bodyComponents[entity]['mainhand']]['maxSpeed']}", fg=colour.WHITE, bg=None)
                        screen.printLine(self.level.width - 22, y + 2, " " * int(8 * (initComponents[bodyComponents[entity]['mainhand']]['speed']/initComponents[bodyComponents[entity]['mainhand']]['maxSpeed'])), fg=None, bg=colour.GREY)
            else:
                screen.printLine(self.level.width - 12, y + 2, 'None', colour.GREY)
            
            screen.printLine(self.level.width - 22, y + 2, 'Mainhand: ', bg=None)


            # --------
            # offhand
            if bodyComponents[entity]['offhand']:
                screen.printLine(self.level.width - 12, y + 3, renderComponents[bodyComponents[entity]['offhand']]['name'], renderComponents[bodyComponents[entity]['offhand']]['fg'], bg=None)
                
                if self.level.e.hasComponent(bodyComponents[entity]['offhand'], Init):
                    # if not initComponents[bodyComponents[entity]['offhand']]['speed']:
                        # screen.draw(self.level.width - 24, y + 3, 'o', colour.GREEN)
                    # else:
                        # screen.draw(self.level.width - 24, y + 3, 'o', colour.RED)
                    if initComponents[bodyComponents[entity]['offhand']]['speed']:
                        screen.printLine(self.level.width - 22, y + 3, " " * int(8 * (initComponents[bodyComponents[entity]['offhand']]['speed']/initComponents[bodyComponents[entity]['offhand']]['maxSpeed'])), fg=None, bg=colour.GREY)
            else:
                screen.printLine(self.level.width - 12, y + 3, 'None', colour.GREY)
            
            screen.printLine(self.level.width - 22, y + 3, ' Offhand: ', bg=None)

            # --------
            # health
            hp = int(20 * (statsComponents[entity]['hp'] / statsComponents[entity]['maxHp']))
            if hp < 8:
                bg = colour.RED
            elif hp < 14:
                bg = colour.YELLOW
            else:
                bg = colour.GREEN

            screen.printLine(self.level.width - 22, y + 5, 'Health:')
            screen.printLine(self.level.width - 22, y + 6, ' ' * hp, fg=None, bg=bg)
            screen.printLine(self.level.width - 22, y + 6, f"{statsComponents[entity]['hp']} / {statsComponents[entity]['maxHp']}", fg=colour.BLACK, bg=None)
            # --------
            # stamina
            # screen.printLine(self.level.width - 22, y + 7, 'Stamina')

            # if initComponents[entity]['maxSpeed']:
            #     speed = int(20 * (initComponents[entity]['speed'] / initComponents[entity]['maxSpeed']))
                # screen.printLine(self.level.width - 24, y + 7, 'o', fg=colour.RED)
                # screen.printLine(self.level.width - 22, y + 8, ' ' * speed, fg=None, bg=colour.RED)
                # screen.printLine(self.level.width - 22, y + 8, f"{initComponents[entity]['speed']}", fg=colour.BLACK, bg=None)
            # else:
                # screen.printLine(self.level.width - 24, y + 7, 'o', fg=colour.GREEN)

            # --------
            # target
            if targetComponents[entity]['target']:
                screen.printLine(
                    self.level.width - 22,
                    y + 9,
                    f"Target: {renderComponents[targetComponents[entity]['target']]['name']}"
                )
                hp = int(20 * (statsComponents[targetComponents[entity]['target']]['hp'] / statsComponents[targetComponents[entity]['target']]['maxHp']))
                screen.printLine(self.level.width - 22, y + 10, ' ' * hp, fg=None, bg=colour.RED)    
                screen.printLine(self.level.width - 22, y + 10, f"{statsComponents[targetComponents[entity]['target']]['hp']} / {statsComponents[targetComponents[entity]['target']]['maxHp']}", fg=colour.WHITE, bg=None)










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
                    selectionComponents[entity]['title'],
                    fg=selectionComponents[entity]['fg'],
                    bg=selectionComponents[entity]['bg'],
                    style='topleft'
                    )

                # draw the list of items
                for i in range(len(selectionComponents[entity]['items'])):
                    title = renderComponents[selectionComponents[entity]['items'][i]]['name']
                    if selectionComponents[entity]['items'][i] in equippedComponents.keys():
                        title += "-" + equippedComponents[selectionComponents[entity]['items'][i]]['slot']

                    screen.printLine(
                        positionComponents[entity]['x']+2,
                        positionComponents[entity]['y']+2+i,
                        title,
                        renderComponents[selectionComponents[entity]['items'][i]]['fg'],
                        colour.GREY if selectionComponents[entity]['selectionIndex'] == i else None
                    )     


