from Components import IsEffect, Render, Position
from Systems.BaseSystem import BaseSystem


class CreateEffectsSystem(BaseSystem):
    actions = ['create_effect']
    alwaysActive=False
    priority = 260

    def run(self):
        renderComponents = self.getComponents(Render)
        effectComponents = self.getComponents(IsEffect)
        
        for action in self.actionQueue:
            x = action['x']
            y = action['y']
            if action['type'] == 'label':
                entity = self.level.e.spawn('Effect-Label', x, y)

                effectComponents[entity]['name'] = action['name']
                if 'fg' in action.keys():
                    renderComponents[entity]['fg'] = action['fg']
                if 'bg' in action.keys():
                    renderComponents[entity]['bg'] = action['bg']

