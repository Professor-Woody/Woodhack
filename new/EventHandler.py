import tcod
from EventActions import *

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, app):
        super().__init__()
        self.app = app

    def ev_quit(self, event: tcod.event.Quit):
        return QuitAction()

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        return KeyAction(self.app, key, True)

    def ev_keyup(self, event: tcod.event.KeyUp):
        key = event.sym
        return KeyAction(self.app, key, False)

    def ev_mousemotion(self, event: tcod.event.MouseMotion):
        self.app.screen.context.convert_event(event)
        