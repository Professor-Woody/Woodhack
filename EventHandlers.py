import tcod
from Actions import Action, KeyAction


class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit):
        raise SystemExit()

    # keypress events
    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        return  KeyAction(key, True)

    def ev_keyup(self, event: tcod.event.KeyUp):
        key = event.sym
        return KeyAction(key, False)


