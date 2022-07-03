from Systems.BaseSystem import BaseSystem
from Components.FlagComponents import IsReady

class UseSystem(BaseSystem):
    def run(self):
        for action in self.actionQueue:
            item = action.item
            useType = action.useType
            entity = action.entity
            
            if item.has(IsReady):
                item.fire_event('use', {'useType': useType, 'entity': entity})
    
        self.actionQueue.clear()

