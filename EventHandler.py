import tcod
from Actions.BaseActions import Action, QuitAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, app, test=False):
        super().__init__()
        self.app = app
        self.test = test

    def ev_quit(self, event: tcod.event.Quit):
        return QuitAction()

    def ev_keydown(self, event: tcod.event.KeyDown):
        if self.test:
            return RegenMapAction(self.app)


class RegenMapAction:
    def __init__(self, app):
        self.app = app

    def perform(self):
        self.app.regenerateLevel()