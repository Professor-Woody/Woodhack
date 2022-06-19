from Actions.BaseActions import EntityAction
from Actions.UIActions import CancelSelectionUIAction

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
                        'use': InventoryDropAction(selectionUI),
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

class InventoryDropAction(EntityAction):
    def perform(self):
        item = self.entity['SelectionUI'].items[self.entity['SelectionUI'].choice]
        self.entity['SelectionUI'].parentEntity['Inventory'].contents.remove(item)
        item.add('Position', {'x': self.entity['SelectionUI'].parentEntity['Position'].x, 'y': self.entity['SelectionUI'].parentEntity['Position'].y})

class SwapEquippedItemAction(EntityAction):
    def __init__(self, entity, equipmentSlot):
        super().__init__(entity)
        self.equipmentSlot = equipmentSlot

    def perform(self):
        item = self.entity['SelectionUI'].items[self.entity['SelectionUI'].choice]
        entity = self.entity['SelectionUI'].parentEntity

        if not item.has('IsEquippable'):
            return

        if not self.equipmentSlot:
            self.equipmentSlot = item['IsEquippable'].equipmentSlot

        if not entity.has(self.equipmentSlot):
            return

        if entity[self.equipmentSlot].equipped:
            entity[self.equipmentSlot].equipped.remove('IsEquipped')
            
        item.add('IsEquipped')
        entity[self.equipmentSlot].equipped = item
