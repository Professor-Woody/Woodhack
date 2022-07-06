from Actions.BaseActions import UpdateLightingAction
from Components.Components import Initiative
from Components.FlagComponents import IsReady
from Systems.BaseSystem import BaseSystem
from Controllers import controllers

class UpdateSystem(BaseSystem):
    def run(self):
        for controller in controllers:
            controller.update()

        for entity in self.level.world.create_query(all_of=['Initiative'], none_of=['IsReady']).result:
            entity[Initiative].speed -= 1
            if not entity[Initiative].speed:
                entity.add(IsReady)
                print ("readying")
        
        lightingUpdated = False
        for action in self.actionQueue:
            if type(action) == UpdateLightingAction and not lightingUpdated:
                print ("updated lighting")
                self.level.map.update()
                lightingUpdated = True
        self.actionQueue.clear()