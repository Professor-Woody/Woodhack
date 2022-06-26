from Components.Components import Render, Position
from Components.UIComponents import SelectionWindowUI
from Systems.BaseSystem import BaseSystem
import Colours as colour

class RenderSystem(BaseSystem):
    def run(self):
        # print ("render start")

        # in theory we'll do this for each render level. for now do map, items, npcs, player, UI
        self.level.map.draw(self.level.app.screen)
        
        entities = []
        entityTypes = ['IsItem', 'IsNPC', 'IsPlayer'] # render order
        for entityType in entityTypes:
            entities.append(self.level.world.create_query(all_of=['Render', entityType, 'Position']).result)            

        for entity in entities:
            self.entityDraw(entity)

        entities = self.level.world.create_query(all_of=['Render', 'IsUI', 'Position']).result
        for entity in entities:
            self.uiDraw(entity)


    def entityDraw(self, entity):
        if entity[Render].needsVisibility and self.level.map.checkIsVisible(entity):
            self.screen.draw(entity)
        elif not entity[Render].needsVisibility:
            self.screen.draw(entity)


    def uiDraw(self, entity):
        # render it's box
        self.screen.drawFrame(entity[Position].x, entity[Position].y, entity[Position].width, entity[Position].height, title=entity[Render].entityName, bg=colour.GREY)
        # render it's contents
        if entity.has(SelectionWindowUI):
            for i in range(len(entity[SelectionWindowUI].selectionData)):
                bg = colour.BLACK
                if i == entity[SelectionWindowUI].selectionIndex:
                    bg = colour.GREY

                self.screen.printLine(
                    entity[Position].x+1, 
                    entity[Position].y+1+i,
                    entity[SelectionWindowUI].selectionData[i][Render].entityName,
                    bg=bg
                    )

    @property
    def screen(self):
        return self.level.app.screen