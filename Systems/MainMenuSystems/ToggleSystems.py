from Components import CharacterSelectPane, Parent, Render, Selected, ToggleUI
from Systems.BaseSystem import BaseSystem


class UpdateTogglesSystem(BaseSystem):
    actions=['player_input']
    priority=50

    def run(self):
        if self._actionQueue:
            toggleComponents = self.getComponents(ToggleUI)
            parentComponents = self.getComponents(Parent)

            for action in self.actionQueue:
                # toggle entity should have a component that contains it's
                # total list of choices and the current index
                parentEntity = action['entity']
                entity = None

                for ui in self.level.childEntitiesQuery.result:
                    if parentComponents[ui]['entity'] == parentEntity:
                        if self.level.e.hasComponent(ui, Selected):
                            entity = ui
                            break
                
                if entity and self.level.e.hasComponent(entity, ToggleUI):
                    command = action['command']

                    if command == 'left':
                        toggleComponents[entity]['index'] -= 1
                        if toggleComponents[entity]['index'] < 0:
                            toggleComponents[entity]['index'] = len(toggleComponents[entity]['labels']) -1
                        self.level.post(toggleComponents[entity]['action'], {'entity': parentEntity, 'selection': toggleComponents[entity]['selection'][toggleComponents[entity]['index']], 'command':command})
                    
                    elif command == 'right':
                        toggleComponents[entity]['index'] += 1
                        if toggleComponents[entity]['index'] >= len(toggleComponents[entity]['labels']):
                            toggleComponents[entity]['index'] = 0
                        self.level.post(toggleComponents[entity]['action'], {'entity': parentEntity, 'selection': toggleComponents[entity]['selection'][toggleComponents[entity]['index']], 'command':command})



class ToggleColourSystem(BaseSystem):
    actions = ['toggle_colour']
    priority=70

    def run(self):
        if self._actionQueue:
            renderComponents = self.getComponents(Render)

            for action in self.actionQueue:
                renderComponents[action['entity']]['fg'] = action['selection']

