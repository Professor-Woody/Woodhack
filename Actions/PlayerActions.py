from Actions.BaseActions import EntityAction
from Actions.InventoryActions import OpenInventoryAction, InventoryAddAction
from Actions.EntityActions import MovementAction, GetTargetAction
from Actions.UIActions import CancelSelectionUIAction

class GetPlayerInputAction(EntityAction):
    def perform(self):
            #  ----------------------
            # start by checking any controls that are not speed dependent
            # check targetting
            target = None
            if self.entity['PlayerInput'].controller.getPressedOnce("next"):
                target = "next"
            elif self.entity['PlayerInput'].controller.getPressedOnce("previous"):
                target = "previous"
            elif self.entity['PlayerInput'].controller.getPressedOnce("nearestEnemy"):
                target = "nearestEnemy"
            if target:
                GetTargetAction(self.entity, target).perform()


            # check use actions (IE equipment)
            if self.entity['PlayerInput'].controller.getPressedOnce('inventory'):
                OpenInventoryAction(self.entity).perform()
            if self.entity['PlayerInput'].controller.getPressedOnce('use'):
                PickupItemAction(self.entity).perform()



            # now check all those that require the player to be ready
            # if required, do one of these (in order of importance)
            #   Move
            #   melee attack
            #   use equipped item

            #  ----------------------
            # check movement
            dx = 0
            dy = 0
            if self.entity['PlayerInput'].controller.getPressed("up"):
                dy -= 1
            if self.entity['PlayerInput'].controller.getPressed("down"):
                dy += 1
            if self.entity['PlayerInput'].controller.getPressed("left"):
                dx -= 1
            if self.entity['PlayerInput'].controller.getPressed("right"):
                dx += 1

            if dx or dy:
                return MovementAction(self.entity['Position'], dx, dy, self.entity['Stats'].moveSpeed).perform()

            #  ----------------------
            #  melee attack
            # check if the targetted monster is within melee range
            target = self.entity['Target'].target
            if target and self.entity['Position'].getRange(target) == 1:            
                return MeleeAttackAction(self).perform()

            #  ----------------------
            #  use equipped item
            elif self.entity['PlayerInput'].controller.getPressed('lefthand') and self.entity['Body'].equipmentSlots['lefthand']:
                self.entity['Body'].equipmentSlots['lefthand'].fire_event('use')


class PickupItemAction(EntityAction):
    def perform(self):
        allItems = self.entity.world.create_query(all_of=['IsItem', 'Position']).result
        items = []
        # check that it's in the same space as our player
        items = list(filter(lambda item: item['Collision'].pointCollides(self.entity['Position'].x, self.entity['Position'].y), allItems))

        
        # now for those on the same space:
        if len(items) == 1:
            item = items[0]
            print (item)
            self.entity['Inventory'].contents.append(item)
            item.remove('Position')

        if len(items) > 1:
            print ("===")
            print (items)
            # create the UI object
            selectionUI = self.entity.world.create_entity()
            selectionUI.add('UI')
            selectionUI.add('SelectionUI', 
                {
                    'parentEntity': self.entity,
                    'items': items, 
                    'actions': {
                        'use': InventoryAddAction(selectionUI),
                        'cancel': CancelSelectionUIAction(selectionUI),
                        }
                })
            selectionUI.add('Position', {'x': self.entity['UIPosition'].sideX, 'y': self.entity['UIPosition'].sideY})

            # lock the player
            self.entity.add('EffectControlsLocked')
