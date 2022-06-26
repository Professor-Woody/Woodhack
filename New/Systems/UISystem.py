from Systems.BaseSystem import BaseSystem
from Actions.TargetActions import GetTargetAction
from Components.Components import PlayerInput, Position, Render
from Components.UIComponents import SelectionWindowUI, Target, Targeted
from Components.FlagComponents import IsUI
from Flags import FPS
from Actions.UIActions import CloseSelectionUIAction, OpenSelectionUIAction, SwapEquippedAction, UpdateUIInputAction

class UISystem(BaseSystem):
    def run(self):
        # -----------------
        # handle any selection UIs
        for action in self.actionQueue:
            if type(action) == OpenSelectionUIAction:
                self.openSelectionUI(action)
            elif type(action) == UpdateUIInputAction:
                self.updateUIInput(action)
            elif type(action) == CloseSelectionUIAction:
                self.closeSelectionUI(action)


    def openSelectionUI(self, action: OpenSelectionUIAction):
        selectionUI = self.level.world.create_entity()
        selectionUI.add(SelectionWindowUI, {
            "parentEntity": action.entity,
            "selectionList": action.selectionList,
            "actions": action.actions
            })
        selectionUI.add(IsUI)
        action.entity[PlayerInput].controlFocus.append(selectionUI)
    
    def closeSelectionUI(self, action):
        selectionUI = action.entity[PlayerInput].controlFocus.pop()
        selectionUI.destroy()


    def updateUIInput(self, action):
        if action.entity.has(SelectionWindowUI):
            return self.updateSelectionWindowUI(action.entity)

    def selectionUISwapEquipped(self, action):
        slot = action.slot
        entity = action.entity
        selectionUI = entity[PlayerInput].controlFocus[-1]
        item = selectionUI[SelectionWindowUI].selectionList[selectionUI[SelectionWindowUI].selectionIndex]
        
        return [
            SwapEquippedAction(entity, slot=slot, item=item),
            CloseSelectionUIAction(selectionUI)
        ]

    def updateSelectionWindowUI(self, entity):
        dy = 0
        # check up
        if entity[SelectionWindowUI].parentEntity[PlayerInput].controller.getPressedOnce('up'):
            dy -= 1
        # check down
        elif entity[SelectionWindowUI].parentEntity[PlayerInput].controller.getPressedOnce('down'):
            dy += 1

        # change index
        entity[SelectionWindowUI].selectionIndex += dy
        if entity[SelectionWindowUI].selectionIndex < 0:
            entity[SelectionWindowUI].selectionIndex = len(entity[SelectionWindowUI].selectionList)-1
        elif entity[SelectionWindowUI].selectionIndex >= len(entity[SelectionWindowUI].selectionList):
            entity[SelectionWindowUI].selectionIndex = 0

        # check actions
            # if action key is pressed
                # return action
        for action in entity[SelectionWindowUI].actions.keys():
            if entity[SelectionWindowUI].parentEntity[PlayerInput].controller.getPressedOnce(action):
                return (entity[SelectionWindowUI].selectionIndex.actions[action])

    





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