from Systems.BaseSystem import BaseSystem


class QuitSystem(BaseSystem):
    actions = ['quit']

    def run(self):
        if self._actionQueue:
            raise SystemExit()