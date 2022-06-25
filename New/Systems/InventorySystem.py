from lib2to3.pytree import Base
from Systems.BaseSystem import BaseSystem
from Actions.InventoryActions import PickupItemAction
from Components.Components import Position, Inventory



class InventorySystem(BaseSystem):
    def run(self):
        for action in self.actionQueue:
            if type(action) == PickupItemAction:
                self.pickupItem(action.entity)
    
        self.actionQueue.clear()

    def pickupItem(self, parentEntity):
        x = parentEntity[Position].x
        y = parentEntity[Position].y

        entities = self.level.world.create_query(all_of=['IsItem', 'Position']).result
        itemsToPickup = []
        for entity in entities:
            if entity[Position].x == x and entity[Position].y == y:
                itemsToPickup.append(entity)
        
        if itemsToPickup:
            if len(itemsToPickup) == 1:
                parentEntity[Inventory].contents.append(itemsToPickup[0])
            # if it's more than one then we'll need to open up a GUI. TODO