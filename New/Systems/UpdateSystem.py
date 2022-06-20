from Components.Components import Initiative
from Components.FlagComponents import IsReady
from Systems.BaseSystem import BaseSystem

class UpdateSystem(BaseSystem):
    def run(self):
        self.level.map.update()

        for entity in self.level.world.create_query(all_of=[Initiative], none_of=[IsReady]).result:
            entity[Initiative].speed -= 1
            if not entity[Initiative].speed:
                entity.add(IsReady)