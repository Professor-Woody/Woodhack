from Systems.BaseSystem import BaseSystem



class TTLSystem(BaseSystem):
    actions=['create_effect']
    priority = 1
    alwaysActive = False
    active = True

    def post(self, action):
        if not self.active:
            self.level.activateSystem(self.priority)
            self.active = True

    def run(self):
        effects = self.level.effectsQuery.result
        entities = self.level.ttlQuery.result
        if effects:
            for entity in entities:
                self.level.post('entity_died', {'entity': entity})
        else:
            self.level.deactivateSystem(self.priority)
            self.active = False