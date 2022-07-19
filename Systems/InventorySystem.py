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



class OpenInventorySystem(BaseSystem):
    actions=['open_inventory']

    def run(self):
        if self._actionQueue:
            inputComponents = self.getComponents(PlayerInput)

            for action in self.actionQueue:
                ui = self.level.e.createEntity()
                items = self.level.e.component.components[Inventory][action['entity']]['contents']

                self.level.e.addComponent(ui, SelectionUI, {
                    'parentEntity': action['entity'],
                    'title': 'Inventory', 
                    'items': items,
                    'commands': {
                        'inventory': {'action': 'close_selection'},
                        'cancel': {'action': 'drop_item'}
                        }
                    })
                self.level.e.addComponent(
                    ui, 
                    Position, 
                    {
                        'x': self.level.width - 22,
                        'y': 0,
                        'width': 22,
                        'height': len(items) + 2    
                    })

                inputComponents[action['entity']]['controlFocus'].append(ui)


class DropItemSystem(BaseSystem):
    actions = ['drop_item']

    def run(self):
        if self._actionQueue:
            
            positionComponents = self.getComponents(Position)

            for action in self.actionQueue:
                item = action['item']
                if item:
                    entity = action['entity']
                    self.level.e.addComponent(item, Position, {
                        'x': positionComponents[entity]['x'],
                        'y': positionComponents[entity]['y']
                    })

                    action['items'].remove(item)

                if 'ui' in action.keys():
                    self.level.post('close_selection', {'ui': action['ui'], 'entity': action['entity']})