from Systems.BaseSystem import BaseSystem
from Actions.TargetActions import GetTargetAction
from Components.Components import Position
from Components.UIComponents import Target, Targeted

class TargetSystem(BaseSystem):
    def run(self):
        # ----------------------
        # perform any actions
        # print ("target start")
        for action in self.actionQueue:
            if type(action) == GetTargetAction:
                    self.getTarget(action)
        self.actionQueue.clear()
        # print ("target end")

    def getTarget(self, action):
        entity = action.entity
        targetType = action.targetType
        targetSelectionOrder = action.targetSelectionOrder

        targets = []
        currentTargetIndex = -1
        for otherEntity in self.level.world.create_query(all_of=['Is' + self.targetType, 'Targeted']).result:
            if self.level.map.checkIsVisible(otherEntity):
                targetRange = entity[Position].getRange(otherEntity)
                targets.append((otherEntity, targetRange))


        targets.sort(key = lambda x: x[1])
        counter = 0
        for otherEntity in targets:
            if otherEntity[0] == entity[Target].target:
                currentTargetIndex = counter
                break
            counter += 1

        entity[Target].target = None
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
            entity[Target].target = finalTarget
            finalTarget[Targeted].targetedBy.add(entity)
        else:
            if entity[Target].target:
                entity[Targeted].targetedBy.remove(entity)
            entity[Target].target = None