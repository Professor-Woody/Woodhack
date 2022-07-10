from Components.FlagComponents import IsEquippable, IsEquipped, IsUI
from Components.PlayerInputComponents import PlayerInput
# from Components.UIComponents import SelectionUI
from ecstremity import Component
from Components.Components import Collision, Position
from ecstremity.entity_event import ECSEvent


class Inventory(Component):
    def __init__(self):
        self.contents = []


    def on_pickup_item(self, action):
        x = action.data.position.x
        y = action.data.position.y
        level = action.data.position.level

        entities = level.world.create_query(all_of=['IsItem', 'Position']).result
        itemsToPickup = [entity for entity in entities if Collision.pointCollides(entity, x, y)]
        
        if itemsToPickup:
            if len(itemsToPickup) == 1:
                self.contents.append(itemsToPickup[0])
                itemsToPickup[0].remove(Position)


    def on_open_inventory(self, action):
        level = self.entity[Position].level
        selectionUI = level.world.create_entity()
        selectionUI.add(IsUI)
        selectionUI.add(Position, {
            "x": level.width - 20,
            "y": 0,
            "width": 20,
            "height": len(self.contents) + 2,
            "level": level
        })
        selectionList = self.contents
        commands = {
            'cancel': ECSEvent('close_UI', target=selectionUI),
            'lefthand': ECSEvent('swap_equipped_from_selection', {'slot': 'lefthand'}, target=self.entity),
            'righthand': ECSEvent('swap_equipped_from_selection', {'slot': 'righthand'}, target=self.entity),
            'inventory': ECSEvent('drop_item_from_selection', target=self.entity),
            'use': ECSEvent('use_item_from_selection', target=self.entity)
        }
        selectionUI.add('SelectionUI', {'parentEntity': self.entity, 'selectionList': selectionList, 'commands': commands})
        self.entity[PlayerInput].controlFocus.append(selectionUI)

    def on_swap_equipped_from_selection(self, action): #
        print ("in on_swap")
        ui = action.source
        item = ui['SelectionUI'].selectionList[ui['SelectionUI'].selectionIndex]
        slot = action.data.slot
        body = self.entity[Body]
        print (f"swapping {item} into {slot}")

        if not item.has(IsEquippable):
            print (f"unable to equip: {item} not IsEquippable")
            # ui.fire_event('close_UI')
            ui.post(ECSEvent('close_UI'))
            return

        if slot in body.slots.keys():
            # get the correct slot for it to go in
            if slot not in item[IsEquippable].slots:
                slot = item[IsEquippable].slots[0]

            # open up the place it will go
            if body.slots[slot]:
                body.slots[slot].remove(IsEquipped)

            # remove it from it's current slot (if any)
            if item.has(IsEquipped):
                body.slots[item[IsEquipped].slot] = None

            # equip it
            body.slots[slot] = item
            item.add(IsEquipped, {"slot": slot})
            # self.entity.fire_event('recalculate_stats')
            self.entity.post(ECSEvent('recalculate_stats'))
            print (f"{item} equipped")
        else:
            print (f"unable to equip: {item}. Body doesn't have {slot}")
        # ui.fire_event('close_UI')
        ui.post(ECSEvent('close_UI'))
        print ("done")

    def on_drop_item_from_selection(self, action): #
        print ("in on_drop")
        ui = action.source
        item = ui['SelectionUI'].selectionList.pop(ui['SelectionUI'].selectionIndex)
        position = self.entity[Position]
        print (f"dropping {item}")

        if item.has(IsEquipped):
            self.entity[Body].slots[item[IsEquipped].slot] = None
            item.remove(IsEquipped)
            # self.entity.fire_event('recalculate_stats')
            self.entity.post(ECSEvent('recalculate_stats'))
        
        item.add(Position, {"x": position.x, "y": position.y, "level": position.level})
        # ui.fire_event("close_UI")
        ui.post(ECSEvent("close_UI"))
        print ("done")

    def on_use_item_from_selection(self, action): #
        print ("in on_use")
        ui = action.source
        item = ui['SelectionUI'].selectionList[ui['SelectionUI'].selectionIndex]

        print (f"using {item}")
        # item.fire_event("use")
        item.post(ECSEvent('use'))
        # ui.fire_event("close_UI")
        ui.post(ECSEvent('close_UI'))
        print ("done")

class Body(Component):
    def __init__(self):
        self.slots = {
            'head': None,
            'body': None,
            'legs': None,
            'feet': None,
            'lefthand': None,
            'righthand': None
        }