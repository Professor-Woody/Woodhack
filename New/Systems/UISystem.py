from Systems.BaseSystem import BaseSystem
from Actions.TargetActions import GetTargetAction
from Components.Components import Position, Render
from Components.UIComponents import Target, Targeted
from Flags import FPS

class TargetSystem(BaseSystem):
    def run(self):
        # ----------------------
        # perform any actions
        # print ("target start")
        if self.actionQueue:
            print (self.actionQueue)
        for action in self.actionQueue:
            if type(action) == GetTargetAction:
                    self.getTarget(action)
        self.actionQueue.clear()
        # print ("target end")

        # now update all the backgrounds of targeted individuals
        self.updateTargeted()

    def updateTargeted(self):
        targeted = self.level.world.create_query(all_of=['Targeted']).result
        for entity in targeted:
            if entity[Targeted].targetedBy:
                if self.level.map.checkIsVisible(entity):
                    entity[Targeted].cooldown -= 1
                    if entity[Targeted].cooldown <= 0:
                        entity[Targeted].cooldown = FPS/2
                        entity[Targeted].targetIndex += 1
                        if entity[Targeted].targetIndex >= len(entity[Targeted].targetedBy):
                            entity[Targeted].targetIndex = 0
                        entity[Render].bg = entity[Targeted].targetedBy[entity[Targeted].targetIndex][Render].fg



    def getTarget(self, action):
        print ("getting target")
        entity = action.entity
        targetType = action.targetType
        targetSelectionOrder = action.targetSelectionOrder

        targets = []
        currentTargetIndex = -1
        for otherEntity in self.level.world.create_query(all_of=['Is' + targetType, 'Targeted']).result:
            if self.level.map.checkIsVisible(otherEntity):
                targetRange = entity[Position].getRange(entity, otherEntity)
                targets.append((otherEntity, targetRange))


        targets.sort(key = lambda x: x[1])
        counter = 0
        for otherEntity in targets:
            if otherEntity[0] == entity[Target].target:
                currentTargetIndex = counter
                break
            counter += 1

        if targets:
            if targetSelectionOrder == "next":
                currentTargetIndex += 1
                if currentTargetIndex > len(targets)-1:
                    currentTargetIndex = 0
            elif targetSelectionOrder == "previous":
                currentTargetIndex -= 1
                if currentTargetIndex < 0:
                    currentTargetIndex = len(targets)-1
            else:
                currentTargetIndex = 0

            finalTarget = targets[currentTargetIndex][0]
            self.removeTargeted(entity)
            entity[Target].target = finalTarget
            if entity not in finalTarget[Targeted].targetedBy:
                finalTarget[Targeted].targetedBy.append(entity)
                finalTarget[Targeted].cooldown = 0
        else:
            self.removeTargeted(entity)

    def removeTargeted(self, entity):
        if entity[Target].target:
            if len(entity[Target].target[Targeted].targetedBy) == 1:
                entity[Target].target[Render].bg = None
            entity[Target].target[Targeted].targetedBy.remove(entity)
            entity[Target].target[Targeted].cooldown = 0
            entity[Target].target = None