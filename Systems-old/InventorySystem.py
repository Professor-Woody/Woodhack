from lib2to3.pytree import Base
from Actions.UIActions import SwapEquippedAction
from Systems.BaseSystem import BaseSystem
from Actions.InventoryActions import PickupItemAction
from Actions.EffectsActions import RecalculateStatsAction
from Components.Components import Body, Position, Inventory



class InventorySystem(BaseSystem):
    def run(self):
        for action in self.actionQueue:
            if type(action) == PickupItemAction:
                self.pickupItem(action.entity)
            elif type(action) == SwapEquippedAction:
                self.swapEquipped(action)
    
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
                itemsToPickup[0].remove(Position)
            # if it's more than one then we'll need to open up a GUI. TODO

    def swapEquipped(self, action):
        slot = action.slot
        entity = action.entity
        item = action.item

        if entity[Body].slots[slot]:
            entity[Inventory].contents.append(entity[Body].slots[slot])
        entity[Body].slots[slot] = item
        print (entity[Body].slots[slot])
        entity[Inventory].contents.remove(item)
        # entity.fire_event("recalculate_stats")
        self.systemsManager.post(RecalculateStatsAction(entity))
    