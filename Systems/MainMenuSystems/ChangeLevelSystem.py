
from Systems.BaseSystem import BaseSystem


class ChangeLevelSystem(BaseSystem):
    actions = ['change_level']

    def run(self):
        if self._actionQueue:

            for action in self.actionQueue:
                self.level.app.changeLevel(action['nextLevel'])
                break
