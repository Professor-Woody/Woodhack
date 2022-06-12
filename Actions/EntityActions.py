from Actions.Actions import Action, EntityAction
from ecstremity.entity import Entity

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
            pass

        # if not then do our best single axis movement
        else:
            if not self.checkCanMove(newLocationX, self.position.y):
                self.dx = 0

            if not self.checkCanMove(self.position.x + self.dx, newLocationY):
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
        print ("targetting")
        targets = []
        currentTargetIndex = -1
        print (self.entity.world.create_query(all_of=['Is' + self.targetType]).result)
        print ('---')
        for entity in self.entity.world.create_query(all_of=['Is' + self.targetType]).result:
            if entity["Position"].level.map.checkIsVisible(entity):
                print (entity)
                targetRange = max(abs(self.entity['Position'].x - entity['Position'].x), abs(self.entity['Position'].y - entity['Position'].y))
                print ('x')
                targets.append((entity, targetRange))


        targets.sort(key = lambda x: x[1])
        print (targets)
        counter = 0
        for entity in targets:
            if entity[0] == self.entity["Target"].target:
                currentTargetIndex = counter
                break
            counter += 1

        self.entity.fire_event("clear_target")
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

            finalTarget = targets[currentTargetIndex][0]
            self.entity.fire_event("set_target", {"target": finalTarget})
            finalTarget.fire_event("add_targeter", {"entity": self.entity})
            print (finalTarget)
        else:
            if self.entity.target:
                self.entity.target.targettedBy.remove(self.entity)
            self.entity.target = None

        print (f"Player {self.entity}\nis now targetting {self.entity['Target'].target}\nfrom list {targets}")




class PickupItemAction(EntityAction):
    def perform(self):
        allItems = self.entity.world.create_query(all_of=['IsItem', 'Position']).result
        items = []
        # check that it's in the same space as our player
        items = list(filter(lambda item: item['Collision'].pointCollides(self.entity['Position'].x, self.entity['Position'].y, allItems)))
        for item in allItems:
            if item['Collision'].pointCollides(self.entity['Position'].x, self.entity['Position'].y):
                items.append(item)

        # now for those on the same space:
        if len(items) == 1:
            item = items[0]
            print (item)
            self.entity['Inventory'].contents.append(item)
            item.remove('Position')

        if len(items) > 1:
            # create the UI object
            selectionUI = self.entity.world.create_entity()
            selectionUI.add('UI')
            selectionUI.add('SelectionUI', 
                {
                    'parentEntity': self.entity,
                    'items': items, 
                    'actions': {
                        'use', InventoryAddAction(self.entity),
                        'cancel', CancelSelectionUIAction(self.entity),
                        }
                })
            selectionUI.add('Position', {'x': self.entity['UIPosition'].sideX, 'y': self.entity['UIPosition'].sideY})

            # lock the player
            self.entity.add('EffectControlsLocked')



