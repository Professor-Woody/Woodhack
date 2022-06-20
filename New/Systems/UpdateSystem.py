from Components.Components import Initiative
from Components.FlagComponents import IsReady

class UpdateSystem:
    def run(self, level):
        level.map.update()

        for entity in level.world.create_query(all_of=[Initiative], none_of=[IsReady]).result:
            entity[Initiative].speed -= 1
            if not entity[Initiative].speed:
                entity.add(IsReady)