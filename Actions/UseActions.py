from Actions.BaseActions import EntityAction


class UseAction(EntityAction):
    def __init__(self, entity, item):
        super().__init__(entity)
        self.item = item


class MeleeAction(EntityAction):
    def __init__(self, entity, item):
        super().__init__(entity)
        self.item = item

class DamageAction(EntityAction):
    def __init__(self, entity, target, damage):
        super().__init__(entity)
        self.target = target
        self.damage = damage
        