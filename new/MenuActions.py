from Action import Action


class MenuAction(Action):
    def __init__(self, app):
        super().__init__()
        self.app = app


class ChangeLevelAction(MenuAction):
    def __init__(self, app, level):
        super().__init__(app)
        self.level = level

    def perform(self):
        print ("changing level")
        self.previousLevel = self.app.level
        self.app.level = self.level


