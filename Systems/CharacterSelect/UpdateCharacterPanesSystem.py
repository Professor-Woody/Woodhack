from Components import AttachedInfoPanel, CharacterSelectPane, PlayerInput, Render, Selected, Target
from Systems.BaseSystem import BaseSystem


class UpdateCharacterPanesSystem(BaseSystem):
    actions = ['player_input']

    def run(self):
        if self._actionQueue:
            paneComponents = self.getComponents(CharacterSelectPane)
            targetComponents = self.getComponents(Target)
            infoPanelComponents = self.getComponents(AttachedInfoPanel)

            for action in self.actionQueue:
                entity = action['entity']
                command = action['command']

                uiEntities = self.level.queries[entity].result

                
                if command == 'up':
                    self.level.e.removeComponent(uiEntities[paneComponents[entity]['selectionIndex']], Selected)
                    paneComponents[entity]['selectionIndex'] -= 1
                    if paneComponents[entity]['selectionIndex'] < 0:
                        paneComponents[entity]['selectionIndex'] = len(uiEntities)-1
                    
                    print (f"{uiEntities[paneComponents[entity]['selectionIndex']]} selected")
                    self.level.e.addComponent(uiEntities[paneComponents[entity]['selectionIndex']], Selected)
                    targetComponents[infoPanelComponents[entity]['entity']]['target'] = uiEntities[paneComponents[entity]['selectionIndex']]


                elif command == 'down':
                    self.level.e.removeComponent(uiEntities[paneComponents[entity]['selectionIndex']], Selected)
                    paneComponents[entity]['selectionIndex'] += 1
                    if paneComponents[entity]['selectionIndex'] >= len(uiEntities):
                        paneComponents[entity]['selectionIndex'] = 0

                    print (f"{uiEntities[paneComponents[entity]['selectionIndex']]} selected")
                    self.level.e.addComponent(uiEntities[paneComponents[entity]['selectionIndex']], Selected)                
                    targetComponents[infoPanelComponents[entity]['entity']]['target'] = uiEntities[paneComponents[entity]['selectionIndex']]


class PanesInputSystem(BaseSystem):
    def run(self):
        entities = self.level.claimedPanesQuery.result
        inputComponents = self.getComponents(PlayerInput)

        commands = [
            'up',
            'down',
            'left',
            'right',
            'use',
            'cancel'
        ]
        for entity in entities:
            # check the input and post the action with the currently selected entity
            inputComponents[entity]['controller'].update()
            for command in commands:
                if inputComponents[entity]['controller'].getPressedOnce(command):
                    print (f"{entity}: {command}")
                    self.level.post('player_input', {
                        'entity': entity,
                        'command': command})

