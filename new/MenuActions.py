from Actions import Action


class MenuAction(Action):
    def __init__(self, app):
        super().__init__()
        self.app = app


class ChangeLevelAction(MenuAction):
    def __init__(self, app, level):
        super().__init__(app)
        self.level = level

    def perform(self):
        print (f"changing level: \n{self.app.previousLevel} \n {self.level}")
        self.app.previousLevel = self.app.level
        self.app.level = self.level


