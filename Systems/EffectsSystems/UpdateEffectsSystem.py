from Systems.BaseSystem import BaseSystem
from Components import IsEffect, IsReady, Render
import Colours as colour

OPENING = 1
OPEN = 2
CLOSING = 3

class UpdateEffectsSystem(BaseSystem):
    priority = 262
    actions = ['create_effect']
    active = True

    
    def post(self, action):
        if not self.active:
            self.level.activateSystem(self.priority)
            self.active = True


    def run(self):        
        entities = self.level.effectsQuery.result

        if not entities:
            self.active = False
            self.level.deactivateSystem(self.priority)
            return

        effectsComponents = self.getComponents(IsEffect)
        renderComponents = self.getComponents(Render)

        for entity in entities:
            # for labels
            # if state == opening, it's extending in size.
            # if opened, it's waiting for the timer to tick down
            # if closing, it's fading out (alpha)
            comp = effectsComponents[entity]

            if comp['state'] == OPENING:
                comp['width']+=1
                #renderComponents[entity]['name'] = f"┤{comp['name'][:comp['width']]}├"
                renderComponents[entity]['name'] = comp['name'][:comp['width']]
                if comp['width'] == len(comp['name']):
                    comp['state'] = OPEN
                    self.level.post('add_speed', {'entity': entity, 'speed': 10})
                    continue

            elif comp['state'] == OPEN:
                if self.level.e.hasComponent(entity, IsReady):
                    renderComponents[entity]['fg'] = colour.GREY
                    renderComponents[entity]['bg'] = colour.GREY
                    self.level.post('add_speed', {'entity': entity, 'speed': 3})
                    comp['state'] = CLOSING

            else:
                print (f"{entity} closing")
                if self.level.e.hasComponent(entity, IsReady):
                    print ("and killing")
                    self.level.post('entity_died', {'entity': entity})




