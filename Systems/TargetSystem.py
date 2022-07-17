from turtle import position
from Systems.BaseSystem import BaseSystem
from Components import *
import Helpers.PositionHelper as PositionHelper

class TargetSystem(BaseSystem):
    actions = ['target']

    def run(self):
        self.highlightTargeted()
        self.targetActions()

    def highlightTargeted(self):
        targetedComponents = self.getComponents(Targeted)
        renderComponents = self.getComponents(Render)

        for targeted, component in targetedComponents.items():
            component['targetTimer']-=1
            if component['targetTimer'] <= 0:
                component['targetTimer'] = 30
                component['targetIndex'] += 1
                if component['targetIndex'] >= len(component['targetedBy']):
                    component['targetIndex'] = 0 
                
                renderComponents[targeted]['bg'] = renderComponents[component['targetedBy'][component['targetIndex']]]['fg']


    def targetActions(self):
        if self._actionQueue:
            targetEntities = self.level.npcsQuery.result
            positionComponents = self.getComponents(Position)
            targetComponents = self.getComponents(Target)

            for action in self.actionQueue:
                targets = []
                currentTargetIndex = -1
                for otherEntity in targetEntities:
                    if self.level.map.checkIsVisible(positionComponents[otherEntity]['x'], positionComponents[otherEntity]['y']):
                        targetRange = PositionHelper.getRange(
                            (positionComponents[action['entity']]['x'], positionComponents[action['entity']]['x']),
                            (positionComponents[otherEntity]['x'], positionComponents[otherEntity]['y'])
                        )
                        targets.append((otherEntity, targetRange))

                if targets:
                    targets.sort(key = lambda x: x[1])
                    print (targets)
                    counter = 0

                    for otherEntity in targets:
                        if otherEntity[0] == targetComponents[action['entity']]['target']:
                            currentTargetIndex = counter
                            break
                        counter += 1

                    if action['targetFocus'] == 'next':
                        currentTargetIndex += 1
                        if currentTargetIndex > len(targets) -1:
                            currentTargetIndex = 0
                    elif action['targetFocus'] == 'previous':
                        currentTargetIndex -= 1
                        if currentTargetIndex < 0:
                            currentTargetIndex = len(targets) - 1
                    else:
                        currentTargetIndex = 0
                    
                    finalTarget = targets[currentTargetIndex][0]

                    if finalTarget != targetComponents[action['entity']]['target']:
                        if targetComponents[action['entity']]['target']:
                            self.level.post('remove_targeter', {
                                'entity': targetComponents[action['entity']]['target'], 
                                'targeter': action['entity']})

                        targetComponents[action['entity']]['target'] = finalTarget
                        self.level.post('add_targeter', {
                            'entity': finalTarget,
                            'targeter': action['entity']
                        })
                else:
                    if targetComponents[action['entity']]['target']:
                        self.level.post('remove_targeter', {
                            'entity': targetComponents[action['entity']]['target'], 
                            'targeter': action['entity']})

                        targetComponents[action['entity']]['target'] = None




class AddTargeterSystem(BaseSystem):
    actions = ['add_targeter']
    
    def run(self):
        if self._actionQueue:
            targetedComponents = self.getComponents(Targeted)

            for action in self.actionQueue:
                if not self.level.e.hasComponent(action['entity'], Targeted):
                    self.level.e.addComponent(action['entity'], Targeted)

                if action['targeter'] not in targetedComponents[action['entity']]['targetedBy']:
                    targetedComponents[action['entity']]['targetedBy'].append(action['targeter'])
                    targetedComponents[action['entity']]['targetTimer'] = 0




class RemoveTargeterSystem(BaseSystem):
    actions = ['remove_targeter']

    def run(self):
        if self._actionQueue:
            targetedComponents = self.getComponents(Targeted)
            renderComponents = self.getComponents(Render)

            for action in self.actionQueue:
                if action['targeter'] in targetedComponents[action['entity']]['targetedBy']:
                    targetedComponents[action['entity']]['targetedBy'].remove(action['targeter'])
                    targetedComponents[action['entity']]['targetTimer'] = 0
                    
                    if not targetedComponents[action['entity']]['targetedBy']:
                        self.level.e.removeComponent(action['entity'], Targeted)
                        renderComponents[action['entity']]['bg'] = None
                        
