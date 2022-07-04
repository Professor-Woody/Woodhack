import tcod
from Actions.BaseActions import Action, QuitAction

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def ev_quit(self, event: tcod.event.Quit):
        return QuitAction()

