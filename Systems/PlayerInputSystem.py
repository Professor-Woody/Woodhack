from Systems.BaseSystem import BaseSystem
from Components import *

class PlayerInputSystem(BaseSystem):
    def run(self):
        entities = self.level.playersQuery.result
        inputComponents = self.level.e.component.filter(PlayerInput, entities)


        