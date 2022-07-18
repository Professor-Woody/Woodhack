from lib2to3.pytree import Base
from Systems.BaseSystem import BaseSystem
from Components import *
import Helpers.PositionHelper as PositionHelper

class TryPickupItemSystem(BaseSystem):
    actions = ['try_pickup_item']
    def run(self):
        if self._actionQueue:
            itemsOnGround = self.level.itemsOnGroundQuery.result
            positionComponents = self.getComponents(Position)

            for action in self.actionQueue:
                # check all items on the ground to see if there's one there to pick up
                entity = action['entity'] # TODO: optimize
                pos = positionComponents[entity]


                # if there's one, pick it up
                items = []
                for item in itemsOnGround:
                    if PositionHelper.pointCollides(positionComponents[item], pos['x'], pos['y']):
                        items.append(item)
                if items:
                    if len(items) == 1:
                        self.level.post('pickup_item', {'entity': entity, 'item': items[0]})
                    else:
                        # if there are multiple, build a list and create a new selectionUI entity
                        print ("too many items on ground. fix your inventory selectionUI Woody")
                        self.level.post('open_selection_ui', {'entity': entity, 'list': items, 'actions': ['pickup_item']})
                        
class PickupItemSystem(BaseSystem):
    actions=['pickup_item']

    def run(self):
        if self._actionQueue:
            inventoryComponents = self.getComponents(Inventory)
            for action in self.actionQueue:
                entity = action['entity']
                item = action['item']
                inventory = inventoryComponents[entity]
                
                inventory['contents'].append(item)
                self.level.e.removeComponent(item, Position)
                print (f"{entity} has picked up {item}")



