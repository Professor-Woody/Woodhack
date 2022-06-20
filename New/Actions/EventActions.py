from New.Actions.BaseActions import Action
import Controllers

class EventAction(Action):
    def __init__(self, app):
        super().__init__()
        self.app = app


class KeyAction(EventAction):
    def __init__(self, app, key, pressed):
        super().__init__(app)
        self.key = key
        self.pressed = pressed

    def perform(self):
        Controllers.keyboardController.setKeyPressed(self.key, self.pressed)


class MouseMotionAction(EventAction):
    def __init__(self, app, x, y):
        super().__init__(app)
        self.x = x
        self.y = y

    def perform(self):
        for uiElement in self.app.level.world.create_query(all_of=['UI']).result:
            uiElement.fire_event('mouse_motion', {'x': self.x, 'y': self.y})

class MouseClickAction(EventAction):
    def __init__(self, app, button, x, y):
        super().__init__(app)
        self.button = button
        self.x = x
        self.y = y

    def perform(self):
        for uiElement in self.app.level.world.create_query(all_of=['UI']).result:
            uiElement.fire_event('mouse_click', {'button': self.button, 'x': self.x, 'y':self.y})
