from lib2to3.pytree import Base
from Systems.BaseSystem import BaseSystem
from Components import *
import Helpers.PositionHelper as PositionHelper
import Colours as colour

class TryPickupItemSystem(BaseSystem):
    actions = ['try_pickup_item']
    def run(self):
        if self._actionQueue:
            itemsOnGround = self.level.itemsOnGroundQuery.result
            positionComponents = self.getComponents(Position)
            renderComponents = self.getComponents(Render)
            idComponents = self.getComponents(IsPlayer)
            inputComponents = self.getComponents(PlayerInput)

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
                        ui = self.level.e.createEntity()

                        self.level.e.addComponent(ui, SelectionUI, {
                            'parentEntity': action['entity'],
                            # 'title': renderComponents[action['entity']]['name'] + '\'s Inventory', 
                            'title': 'Pick up', 
                            'items': items,
                            'commands': {
                                'use': {'action': 'pickup_item'},
                                'mainhand': {'action': 'pickup_item'},
                                'offhand': {'action': 'pickup_item'},
                                'cancel': {'action': 'close_selection'},
                                },
                            'fg': renderComponents[action['entity']]['fg']
                            # 'fg': colour.YELLOW
                            })
                        self.level.e.addComponent(
                            ui, 
                            Position, 
                            {
                                'x': self.level.width - 24,
                                'y': (idComponents[action['entity']]['id']*16),
                                'width': 24,
                                'height': 16
                            })

                        inputComponents[action['entity']]['controlFocus'].append(ui)
                        

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
                self.log(f"£{action['entity']}$ has picked up a £{action['item']}$")
            
            if 'ui' in action.keys():
                    self.level.post('close_selection', {'ui': action['ui'], 'entity': action['entity']})



class OpenInventorySystem(BaseSystem):
    actions=['open_inventory']

    def run(self):
        if self._actionQueue:
            inputComponents = self.getComponents(PlayerInput)
            idComponents = self.getComponents(IsPlayer)
            renderComponents = self.getComponents(Render)

            for action in self.actionQueue:
                ui = self.level.e.createEntity()
                items = self.level.e.component.components[Inventory][action['entity']]['contents']

                self.level.e.addComponent(ui, SelectionUI, {
                    'parentEntity': action['entity'],
                    # 'title': renderComponents[action['entity']]['name'] + '\'s Inventory', 
                    'title': 'Inventory', 
                    'items': items,
                    'commands': {
                        'inventory': {'action': 'close_selection'},
                        'use': {'action': 'use_item'},
                        'mainhand': {'action': 'equip_item', 'data': {'slot': 'mainhand'}},
                        'offhand': {'action': 'equip_item', 'data': {'slot': 'offhand'}},
                        'cancel': {'action': 'drop_item'},
                        'nearestEnemy': {'action': 'inspect_item'}
                        },
                    'fg': renderComponents[action['entity']]['fg']
                    # 'fg': colour.YELLOW
                    })
                self.level.e.addComponent(
                    ui, 
                    Position, 
                    {
                        'x': self.level.width - 24,
                        'y': (idComponents[action['entity']]['id']*16)+1,
                        'width': 24,
                        'height': 15
                    })

                inputComponents[action['entity']]['controlFocus'].append(ui)


class DropItemSystem(BaseSystem):
    actions = ['drop_item']

    def run(self):
        if self._actionQueue:
            
            positionComponents = self.getComponents(Position)
            bodyComponents = self.getComponents(Body)
            equippedComponents = self.getComponents(Equipped)

            for action in self.actionQueue:
                item = action['item']

                if item:
                    entity = action['entity']
                    if self.level.e.hasComponent(item, Equipped):
                        bodyComponents[entity][equippedComponents[item]['slot']] = None
                        print (f"removing {item} from {equippedComponents[item]['slot']}")
                        print (bodyComponents[entity])
                        self.level.e.removeComponent(item, Equipped)
                        self.level.post('recalculate_stats', {'entity': action['entity']})
                    else:
                        print (f"{item} was not equipped")

                    self.level.e.addComponent(item, Position, {
                        'x': positionComponents[entity]['x'],
                        'y': positionComponents[entity]['y']
                    })

                    self.log(f"£{action['entity']}$ has dropped a £{action['item']}$")

                    action['items'].remove(item)

                if 'ui' in action.keys():
                    self.level.post('close_selection', {'ui': action['ui'], 'entity': action['entity']})


class EquipItemSystem(BaseSystem):
    actions = ['equip_item']

    def run(self):
        if self._actionQueue:
            bodyComponents = self.getComponents(Body)
            equipComponents = self.getComponents(Equip)
            equippedComponents = self.getComponents(Equipped)

            for action in self.actionQueue:
                if action['item']:
                    if self.level.e.hasComponent(action['item'], Equip):
                        if 'slot' in action.keys():
                            if action['slot'] in equipComponents[action['item']]['slots']:
                                # the item can be put into the defined slot
                                slot = action['slot']
                                print (f"{action['item']} added to {action['slot']}")
                            else:
                                # they obviously still want to equip it, so just put it in
                                # the first slot identified in the item list
                                slot = equipComponents[action['item']]['slots'][0]
                                print (f"{action['item']} added to default slot {slot}")
                            
                        else:
                            slot = equipComponents[action['item']]['slots'][0]
                            print (f"{action['item']} added to default slot {slot}")
                        
                        self.removeItem(bodyComponents, action['entity'], slot)
                        self.addItem(bodyComponents, equippedComponents, action['entity'], action['item'], slot)
                        
                        self.log(f"£{action['entity']}$ has equipped a £{action['item']}$")

                        self.level.post('recalculate_stats', {'entity': action['entity']})

                if 'ui' in action.keys():
                    self.level.post('close_selection', {'ui': action['ui'], 'entity': action['entity']})


    def removeItem(self, bodyComponents, entity, slot):
        if bodyComponents[entity][slot]:
            self.level.e.removeComponent(bodyComponents[entity][slot], Equipped)
            bodyComponents[entity][slot] = None

    def addItem(self, bodyComponents, equippedComponents, entity, item, slot):
        if item in equippedComponents.keys():
            self.removeItem(bodyComponents, entity, equippedComponents[item]['slot'])

        bodyComponents[entity][slot] = item
        self.level.e.addComponent(item, Equipped, {'slot': slot})
