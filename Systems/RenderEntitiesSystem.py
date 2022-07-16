from Components import *
from Systems.BaseSystem import BaseSystem

class RenderEntitiesSystem(BaseSystem):
    def run(self):
        entities = self.level.renderQuery.result
        renderComponents = self.level.e.component.filter(Render, entities)
        positionComponents = self.level.e.component.filter(Position, entities)
        screen = self.level.app.screen

        for entity in entities:
            screen.draw(
                positionComponents[entity]['x'], 
                positionComponents[entity]['y'],
                renderComponents[entity]['char'],
                renderComponents[entity]['fg'])
            