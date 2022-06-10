from Actions.Actions import Action


class EntityAction(Action):
    def __init__(self, entity):
        super().__init__()
        self.entity = entity


class WaitAction(EntityAction):
    def __init__(self, entity, time):
        super().__init__(entity)
        self.time = time

    def perform(self):
        self.entity.speed += self.time


class CheerAction(EntityAction):
    def __init__(self, entity, msg):
        super().__init__(entity)
        self.msg = msg

    def perform(self):
        print(self.msg)


class WatchAction(WaitAction):
    def perform(self):
        print (self.entity.name + "is watching")
        if self.entity.level.map.checkIsVisible(self.entity):
            for player in self.entity.level.entityManager.players:
                if player == self.entity:
                    continue
                if not self.entity.target:
                    self.entity.target = player
                else:
                    if self.getDistance(player) < self.getDistance(self.entity.target):
                        self.entity.target = player
        else:
            if not self.entity.target:
                super().perform()        
    
    def getDistance(self, target):
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        return max(abs(dx, abs(dy)))


class MovementAction(Action):
    def __init__(self, position, dx, dy, speed):
        super().__init__()
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.position = position

    def perform(self):
        # first check if we can diagonally move
        newLocationX = self.position.x + self.dx
        newLocationY = self.position.y + self.dy
        if self.checkCanMove(newLocationX, newLocationY):
            print ("option A")
            pass

        # if not then do our best single axis movement
        else:
            if not self.checkCanMove(newLocationX, self.position.y):
                self.dx = 0
                print ("option B")

            if not self.checkCanMove(self.position.x + self.dx, newLocationY):
                print ("option C")
                self.dy = 0

        if self.dx or self.dy:
            self.position.entity.fire_event("move", {"x":self.position.x + self.dx, "y": self.position.y + self.dy})
            self.position.entity.fire_event("add_initiative", {"speed": self.speed})


    def checkCanMove(self, dx, dy):
        if not self.position.level or \
            not self.position.level.map.checkInBounds(dx, dy) or \
            not self.position.level.map.checkIsPassable(dx, dy) or \
            self.position.level.map.checkIsBlocked(dx, dy):
            return False
        return True



class GetTargetAction(EntityAction):
    def __init__(self, entity, targetRange, targetType="NPC"):
        super().__init__(entity)
        self.targetType = targetType
        self.targetRange = targetRange

    def perform(self):
        targets = []
        currentTargetIndex = -1

        for entity in self.entity.world.create_query(all_of=[self.targetType]).result:
            if entity["Position"].level.map.checkIsVisible(entity):
                targetRange = max(abs(self.entity.x - entity.x), abs(self.entity.y - entity.y))
                targets.append((entity, targetRange))

        targets.sort(key = lambda x: x[1])
        
        counter = 0
        for entity in targets:
            if entity[0] == self.entity["Target"].target:
                currentTargetIndex = counter
                break
            counter += 1

        if targets:
            if self.targetRange == "next":
                currentTargetIndex += 1
                if currentTargetIndex > len(targets)-1:
                    currentTargetIndex = 0
            elif self.targetRange == "previous":
                currentTargetIndex -= 1
                if currentTargetIndex < 0:
                    currentTargetIndex = len(targets)-1
            else:
                currentTargetIndex = 0

            
            self.entity.fire_event("clear_target")

            finalTarget = targets[currentTargetIndex][0]
            self.entity.fire_event("set_target", {"target": finalTarget})
            finalTarget.fire_event("add_targeter", {"entity": self.entity})

        else:
            if self.entity.target:
                self.entity.target.targettedBy.remove(self.entity)
            self.entity.target = None

        print (f"Player {self.entity}\nis now targetting {self.entity['Target'].target}\nfrom list {targets}")

class GetPlayerInputAction(EntityAction):
    def perform(self):
            # check menu

            
            # check movement
            dx = 0
            dy = 0
            if self.entity[PlayerInput].controller.getPressed("up"):
                dy -= 1
            if self.entity[PlayerInput].controller.getPressed("down"):
                dy += 1
            if self.entity[PlayerInput].controller.getPressed("left"):
                dx -= 1
            if self.entity[PlayerInput].controller.getPressed("right"):
                dx += 1

            if dx or dy:
                MovementAction(self.entity[Position], dx, dy, self.entity[Stats].moveSpeed).perform()            

            # check use actions (IE equipment)
            if self.entity[PlayerInput].controller.getPressed('inventory'):
                OpenInventoryAction(self.entity).perform()
            # print (3)

            # check targetting
            target = None
            if self.entity[PlayerInput].controller.getPressedOnce("next"):
                target = "next"
            elif self.entity[PlayerInput].controller.getPressedOnce("previous"):
                target = "previous"
            elif self.entity[PlayerInput].controller.getPressedOnce("nearestEnemy"):
                target = "nearestEnemy"
            # print (target)
            if target:
                GetTargetAction(self.entity, target).perform()
            # print (4)

class PickupItemAction(EntityAction):
    def perform(self):
        items = self.entity.world.create_query(['IsItem']).result
        if len(items) == 1:
            item = items[0]
            self.entity['Inventory'].contents.add(item)
            item.remove('Position')

        if len(items) > 1:
            # create the UI object
            selectionUI = self.entity.world.create_entity()
            selectionUI.add('UI')
            selectionUI.add('SelectionUI', 
                {'entity': self.entity, 
                'items': items, 
                'actions': {
                    'use', InventoryAddAction(self.entity),
                    'cancel', CancelSelectionUIAction(self.entity),
                    }
            })
            selectionUI.add('Position', {'x': self.entity['UIPosition'].sideX, 'y': self.entity['UIPosition'].sideY})

            # lock the player
            self.entity.add('EffectControlsLocked')


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
                    'entity': self.entity,
                    'items': items,
                    'actions': {
                        'use': InventoryDropAction(self.entity),
                        'cancel': CancelSelectionUIAction(self.entity),
                        'lefthand': SwapEquippedItemAction(self.entity, 'lefthand'),
                        'righthand': SwapEquippedItemAction(self.entity, 'righthand')
                    }
                })
            selectionUI.add(
                'Position',
                {
                    'x': self.entity['UIPosition'].sideX, 
                    'y': self.entity['UIPosition'].sideY,
                })


class GetSelectionInput(EntityAction):
    def perform(self):
        dy = 0
        if self.entity['SelectionUI'].entity['PlayerInput'].controller.getPressedOnce("up"):
            dy -= 1
        if self.entity['SelectionUI'].entity['PlayerInput'].controller.getPressedOnce("down"):
            dy += 1
        if dy:
            self.entity['SelectionUI'].choice += dy
            if self.entity['SelectionUI'].choice < 0:
                self.entity['SelectionUI'].choice = len(self.entity['SelectionUI'].items)-1
            elif self.entity['SelectionUI'].choice >= len(self.entity['SelectionUI'].items):
                self.entity['SelectionUI'].choice = 0

        for action in self.entity['SelectionUI'].actions:
            if self.entity['SelectionUI'].entity['PlayerInput'].controller.getPressedOnce(action):
                self.entity['SelectionUI'].actions[action].perform()

class CancelSelectionUIAction(EntityAction):
    def perform(self):
        self.entity['SelectionUI'].entity.remove('EffectControlsLocked')
        self.entity.destroy()


class InventoryAddAction(EntityAction):
    def perform(self):
        item = self.entity['SelectionUI'].items[self.entity['SelectionUI'].choice]
        self.entity['SelectionUI'].entity['Inventory'].contents.add(item)
        item.remove('Position')

class InventoryDropAction(EntityAction):
    def perform(self):
        item = self.entity['SelectionUI'].items[self.entity['SelectionUI'].choice]
        self.entity['SelectionUI'].entity['Inventory'].contents.remove(item)
        item.add('Position', {'x': self.entity['SelectionUI'].entity['Position'].x, 'y': self.entity['SelectionUI'].entity['Position'].y})

class SwapEquippedItemAction(EntityAction):
    def __init__(self, entity, hand):
        super().__init__(entity)
        self.hand = hand

    def perform(self):
        item = self.entity['SelectionUI'].items[self.entity['SelectionUI'].choice]
        entity = self.entity['SelectionUI'].entity

        if entity[self.hand].equipped:
            item = entity['Inventory'].pop(self.entity['SelectionUI'].choice)
            entity['Inventory'].contents.add(self.entity[self.hand].equipped)
            entity[self.hand].equipped = item
