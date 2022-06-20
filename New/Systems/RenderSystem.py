from Components.Components import Render, Position

class RenderSystem:
    def run(self, level):
        level.map.draw(level.app.screen)
        
        # in theory we'll do this for each render level
        entities = level.world.create_query(all_of=[Render, Position]).result

        for entity in entities:
            if entity[Render].needsVisibility and level.map.checkIsVisible(entity):
                level.app.screen.draw(entity)
            elif not entity[Render].needsVisibility:
                level.app.screen.draw(entity)
