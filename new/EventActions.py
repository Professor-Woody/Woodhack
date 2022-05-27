from Actions import Action

class EventAction(Action):
    def __init__(self, app):
        super().__init__()
        self.app = app


class QuitAction(EventAction):
    def perform(self):
        print ("Quitting")
        raise SystemExit()


class KeyAction(EventAction):
    def __init__(self, app, key, pressed):
        super().__init__(app)
        self.key = key
        self.pressed = pressed

    def perform(self):
        self.app.keyboardController.setKey(self.key, self.pressed)


class MouseMotionAction(EventAction):
    def __init__(self, app, x, y):
        super().__init__(app)
        self.x = x
        self.y = y

    def perform(self):
        for uiElement in self.app.level.entityManager.ui:
            uiElement.mouseMotion(self.x, self.y)

class MouseClickAction(EventAction):
    def __init__(self, app, button, x, y):
        super().__init__(app)
        self.button = button
        self.x = x
        self.y = y

    def perform(self):
        for uiElement in self.app.level.entityManager.ui:
            uiElement.mouseClick(self.button, self.x, self.y)