import tcod
from Actions import Action, KeyAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, app):
        super().__init__()
        self.app = app
        
    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()

    # keypress events
    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        return  KeyAction(key, True, self.app)

    def ev_keyup(self, event: tcod.event.KeyUp):
        key = event.sym
        return KeyAction(key, False, self.app)


