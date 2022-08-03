import tcod
from Actions.BaseActions import Action, QuitAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def ev_quit(self, event: tcod.event.Quit):
        return QuitAction()

    # def ev_keydown(self, event: tcod.event.KeyDown):
    #     return RegenMapAction(self.app)


class RegenMapAction:
    def __init__(self, app):
        self.app = app

    def perform(self):
        self.app.regenerateLevel()