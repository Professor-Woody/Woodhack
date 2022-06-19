from Actions.BaseActions import Action, EntityAction
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
        targets = []
        currentTargetIndex = -1
        for entity in self.entity.world.create_query(all_of=['Is' + self.targetType]).result:
            if entity["Position"].level.map.checkIsVisible(entity):
                # targetRange = max(abs(self.entity['Position'].x - entity['Position'].x), abs(self.entity['Position'].y - entity['Position'].y))
                targetRange = self.entity['Position'].getRange(entity)
                targets.append((entity, targetRange))


        targets.sort(key = lambda x: x[1])
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
        else:
            if self.entity.target:
                self.entity.target.targettedBy.remove(self.entity)
            self.entity.target = None

class MeleeAttackAction(EntityAction):
    def perform(self):
        target = self.entity['IsEquipped'].parentEntity['Target'].target

        for slot in ['lefthand', 'righthand']:
            item = self.entity['IsEquipped'].parentEntity['Body'].equipmentSlots[key]

            if item and item.has('Melee') and item.has('IsReady'):
                # do something attacky
                # check if hit
                hitRoll = random.randint(-9, 10) + item['Melee'].attack + self.entity['IsEquipped'].parentEntity['Stats'].attack

                # if hit, roll damage
                if hitRoll >= target['Stats'].defence:
                    damage = sum( [ random.randint(1, item['Melee'].diceType) for x in range(item['Melee'].diceAmount) ] ) + item['Melee'].damageBonus + self.entity['Stats'].bonusDamage
                    self.entity['IsEquipped'].parentEntity.fire_event('add_initiative', {'speed': item['Melee'].attackSpeed})
                    self.entity.fire_event('add_initiative', {'speed': item['Melee'].attackSpeed + 1})
                    # apply damage
                    target.fire_event('damage', {"damage": damage})
                    #  PRINT SOMETHING PITHY HERE!

                    

class RangedAttackAction(EntityAction):
    def perform(self):
        # confirm target
        # confirm ammo TODO
        # confirm visible
        # confirm in range TODO
        # confirm LOS
        
        # roll attack
        # roll damage
        # apply damage
        # spawn effect TODO
        # add speed
    
        parent = self.entity['IsEquipped'].parentEntity
        target = parent['Target'].target
        
        # confirm target
        if target:
            # confirm ammo TODO
            # confirm visible
            if parent['Position'].level.map.checkIsVisible(target):
                # confirm range TODO
                # confirm LOS
                if parent['Position'].getLOS(target):
                    # roll attack
                    print (f"{parent}  is ranged attacking  {target}")
                    attack = random.randint(-9,10) + self.entity['Ranged'].attack + parent['stats'].attack
                    if attack >= target['stats'].defence:
                        # roll damage
                        damage = sum( [ random.randint(1, self.entity['Ranged'].diceType) for x in range(item['Ranged'].diceAmount) ] ) + self.entity['Ranged'].damageBonus + parent['Stats'].bonusDamage
                        parent.fire_event('add_initiative', {'speed': item['Ranged'].attackSpeed})
                        self.entity.fire_event('add_initiative', {'speed': item['Ranged'].attackSpeed + 1})
                        # apply damage
                        target.fire_event('damage', {"damage": damage})
                        #  PRINT SOMETHING PITHY HERE!
                        return
        self.entity['Use'].cancelUse = True




            



class CalculateStatsAction(EntityAction):
    def perform(self):
        # set the stats back to default
        stats = self.entity['stats']
        body = self.entity['body'].equipmentSlots

        maxHp = stats.baseMaxHp
        moveSpeed = stats.baseMoveSpeed
        defence = stats.baseDefence
        attack = stats.baseAttack

        for item in self.entity['Body'].equipmentSlots.values():
            if item:
                if item.has('Defence'):
                    defence += item['Defence'].armour
                if item.has('MoveSpeedModifier'):
                    moveSpeed += item['MoveSpeedModifier'].modifier
                if item.has('AttackModifier'):
                    attack += item['AttackModifier'].modifier
                if item.has('HPModifier'):
                    maxHp += item['HPModifier'].modifier

        stats.maxHp = maxHp
        stats.moveSpeed = moveSpeed
        stats.defence = defence
        stats.attack = attack




