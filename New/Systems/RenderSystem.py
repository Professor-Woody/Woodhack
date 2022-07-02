from Components.Components import Render, Position
from Components.UIComponents import SelectionWindowUI
from Systems.BaseSystem import BaseSystem
import Colours as colour
import time

class RenderSystem(BaseSystem):
    lastTime = time.time()*1000
    fps = 0
    lastFps = 0

    def run(self):

        # in theory we'll do this for each render level. for now do map, items, npcs, player, UI
        self.level.map.draw(self.level.app.screen)
        
        entities = []
        entityTypes = ['IsItem', 'IsNPC', 'IsPlayer']
        for entityType in entityTypes:
            entities += self.level.world.create_query(all_of=['Render', 'Position'], any_of=[entityType]).result

        for entity in entities:
            self.entityDraw(entity)

        entities = self.level.world.create_query(all_of=['Render', 'IsUI', 'Position']).result
        for entity in entities:
            self.uiDraw(entity)

        self.fps += 1
        curTime = time.time()*1000
        if curTime >= self.lastTime + 1000:
            self.lastTime = curTime
            self.lastFps = self.fps
            self.fps = 0
        self.screen.printLine(0,0, str(self.lastFps))




    def entityDraw(self, entity):
        if entity[Render].needsVisibility:
            if self.level.map.checkIsVisible(entity):
                self.screen.draw(entity)
        elif not entity[Render].needsVisibility:
            self.screen.draw(entity)


    def uiDraw(self, entity):
        # render it's box
        self.screen.drawFrame(entity[Position].x, entity[Position].y, entity[Position].width, entity[Position].height, title=entity[Render].entityName, bg=colour.BLACK)
        # render it's contents
        if entity.has(SelectionWindowUI):
            for i in range(len(entity[SelectionWindowUI].selectionList)):
                bg = colour.BLACK
                if i == entity[SelectionWindowUI].selectionIndex:
                    bg = colour.GREY

                self.screen.printLine(
                    entity[Position].x+1, 
                    entity[Position].y+1+i,
                    entity[SelectionWindowUI].selectionList[i][Render].entityName,
                    bg=bg
                    )

    @property
    def screen(self):
        return self.level.app.screen