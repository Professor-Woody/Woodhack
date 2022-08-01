from Systems.BaseSystem import BaseSystem


class QuitSystem(BaseSystem):
    actions = ['quit']
    alwaysActive=False
    priority=5000
    
    def run(self):
        if self._actionQueue:
            raise SystemExit()