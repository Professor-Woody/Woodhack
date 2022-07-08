from Components.PlayerInputComponents import PlayerInput
from Components.UIComponents import SelectionUI
from ecstremity import Component
from Components.Components import Collision, Position

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
        selectionUI = self.entity[Position].level.world.create_entity()
        selectionList = self.contents
        commands = {
            "cancel": ["close_UI", {"UI": selectionUI}]
        }
        selectionUI.add(SelectionUI, {'parentEntity': self.entity, 'selectionList': selectionList, 'commands': commands})
        self.entity[PlayerInput].controlFocus.append(selectionUI)
