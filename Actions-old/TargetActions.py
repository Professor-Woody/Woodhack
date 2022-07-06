from Actions.BaseActions import TargetAction


class GetTargetAction(TargetAction):
    def __init__(self, entity, targetType, targetSelectionOrder):
        super().__init__(entity)
        self.targetType = targetType
        self.targetSelectionOrder = targetSelectionOrder