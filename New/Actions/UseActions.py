from Actions.BaseActions import EntityAction


class UseAction(EntityAction):
    def __init__(self, entity, item, useType):
        super().__init__(entity)
        self.item = item
        self.useType = useType