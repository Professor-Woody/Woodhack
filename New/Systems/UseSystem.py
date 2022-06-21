from Systems.BaseSystem import BaseSystem
from Components.FlagComponents import IsReady

class UseSystem(BaseSystem):
    def run(self):
        # print ("use start")
        for action in self.actionQueue:
            item = action.item
            useType = action.useType
            parentEntity = action.parentEntity
            
            if item.has(IsReady):
                item.fire_event('use', {'useType': useType, 'parentEntity': parentEntity})
        # print ("use end")
    
        self.actionQueue.clear()

