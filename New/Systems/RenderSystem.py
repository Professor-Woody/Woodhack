from Components.Components import Render, Position
from Systems.BaseSystem import BaseSystem

class RenderSystem(BaseSystem):
    def run(self):
        # print ("render start")
        self.level.map.draw(self.level.app.screen)
        
        # in theory we'll do this for each render level
        entities = self.level.world.create_query(all_of=['Render', 'Position']).result

        for entity in entities:
            if entity[Render].needsVisibility and self.level.map.checkIsVisible(entity):
                self.level.app.screen.draw(entity)
            elif not entity[Render].needsVisibility:
                self.level.app.screen.draw(entity)
        # print ("render end")

