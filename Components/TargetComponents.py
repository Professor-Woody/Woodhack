from Components.Components import Position, Render
from ecstremity import Component
from Flags import FPS

class Target(Component):
    target = None

    def on_set_target(self, action):
        targetType = action.data.targetType
        targetSelectionOrder = action.data.targetSelectionOrder
        targets = []
        currentTargetIndex = -1
        for otherEntity in self.entity[Position].level.world.create_query(all_of=['Is' + targetType]).result:
            if self.entity[Position].level.map.checkIsVisible(otherEntity):
                targetRange = Position.getRange(self.entity, otherEntity)
                targets.append((otherEntity, targetRange))
        targets.sort(key = lambda x: x[1])
        counter = 0
        for otherEntity in targets:
            if otherEntity[0] == self.target:
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
            if self.target:
                self.target.fire_event('remove_targeter', {"targeter": self.entity})
            self.target = finalTarget
            self.target.fire_event('add_targeter', {'targeter': self.entity})
            print (f"now targeting {self.target}")
        else:
            if self.target:
                self.target.fire_event('remove_targeter', {'targeter': self.entity})
                self.target = None
            print ("No targets")

class Targeted(Component):
    def __init__(self):
        self.targetedBy = []
        self.targetIndex = 0
        self.cooldown = 0
    
    def on_add_targeter(self, action):
        if action.data.targeter not in self.targetedBy:
            self.targetedBy.append(action.data.targeter)
            self.cooldown = 0

    def on_remove_targeter(self, action):
        if action.data.targeter in self.targetedBy:
            self.targetedBy.remove(action.data.targeter)
            self.cooldown = 0
        if not self.targetedBy:
            self.entity[Render].bg = self.entity[Render].baseBG
            

    def on_update(self, action):
        if self.targetedBy:
            self.cooldown -= 1
            if self.cooldown <= 0:
                self.cooldown = FPS/2
                self.targetIndex -= 1
                if self.targetIndex < 0:
                    self.targetIndex = len(self.targetedBy)-1
                self.entity[Render].bg = self.targetedBy[self.targetIndex][Render].fg


