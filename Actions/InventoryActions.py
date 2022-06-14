from xml.dom.minidom import Entity
from Actions.BaseActions import EntityAction
from Actions.UIActions import CancelSelectionUIAction, DestroyUIAction



class OpenInventoryAction(EntityAction):
    def perform(self):
        items = self.entity['Inventory'].contents
        if len(items):
            self.entity.add('EffectControlsLocked')
            selectionUI = self.entity.world.create_entity()
            selectionUI.add('UI')
            selectionUI.add(
                'SelectionUI',
                {
                    'parentEntity': self.entity,
                    'items': items,
                    'actions': {
                        'inventory': SwapEquippedItemAction(selectionUI, None),
                        'nearestEnemy': InventoryDropAction(selectionUI),
                        'use': InventoryUseItemAction(selectionUI),
                        'cancel': CancelSelectionUIAction(selectionUI),
                        'lefthand': SwapEquippedItemAction(selectionUI, 'lefthand'),
                        'righthand': SwapEquippedItemAction(selectionUI, 'righthand')
                    }
                })
            selectionUI.add(
                'Position',
                {
                    'x': self.entity['UIPosition'].sideX, 
                    'y': self.entity['UIPosition'].sideY,
                })

class InventoryAddAction(EntityAction):
    def perform(self):
        item = self.entity['SelectionUI'].items[self.entity['SelectionUI'].choice]
        self.entity['SelectionUI'].parentEntity['Inventory'].contents.append(item)
        item.remove('Position')
        DestroyUIAction(self.entity)

class InventoryDropAction(EntityAction):
    def perform(self):
        item = self.entity['SelectionUI'].items[self.entity['SelectionUI'].choice]
        self.entity['SelectionUI'].parentEntity['Inventory'].contents.remove(item)
        item.add('Position', {'x': self.entity['SelectionUI'].parentEntity['Position'].x, 'y': self.entity['SelectionUI'].parentEntity['Position'].y})
        
        if item.has('IsEquipped'):
            item.remove('IsEquipped')
            CalculateStatsAction(self.entity['SelectionUI'].parentEntity).perform()       

        DestroyUIAction(self.entity).perform()

class InventoryUseItemAction(EntityAction):
    def perform(self):
        item = self.entity['SelectionUI'].items[self.entity['SelectionUI'].choice]
        for action in item['Use'].actions:
            action.perform(self.entity['SelectionUI'].parentEntity)
        


class SwapEquippedItemAction(EntityAction):
    def __init__(self, entity, equipmentSlot):
        super().__init__(entity)
        self.equipmentSlot = equipmentSlot

    def perform(self):
        item = self.entity['SelectionUI'].items[self.entity['SelectionUI'].choice]
        entity = self.entity['SelectionUI'].parentEntity
        body = self.entity['SelectionUI'].parentEntity['Body'].equipmentSlots

        # confirm the item is equippable
        if not item.has('IsEquippable'):
            return

        # confirm the body has the requisite slot
        if not self.equipmentSlot:  # we haven't confirmed a hand so check the item
            self.equipmentSlot = item['IsEquippable'].equipmentSlot
            if self.equipmentSlot == "anyhand":
                hands = [body['lefthand'], body['righthand']]

                if not hands[1]:
                    self.equipmentSlot = 'righthand'
                else:
                    self.equipmentSlot = 'lefthand'

        # swap the item into the slot
        if body[self.equipmentSlot]:
            body[self.equipmentSlot].remove('IsEquipped')

        body[self.equipmentSlot] = item
        item.add('IsEquipped', {'parentEntity': entity})

        CalculateStatsAction(self.entity['SelectionUI'].parentEntity).perform()
        
        DestroyUIAction(self.entity).perform()

