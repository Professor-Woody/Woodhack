from Actions.Actions import Action
from Entity import Player

class MenuAction(Action):
    def __init__(self, app):
        super().__init__()
        self.app = app


class ChangeLevelAction(MenuAction):
    def __init__(self, app, level):
        super().__init__(app)
        self.level = level

    def perform(self):
        print (f"changing level: \nPrevious: {self.app.previousLevel}\nNew: {self.level}\n")
        self.app.previousLevel = self.app.level
        self.app.level = self.level


class NewGameAction(MenuAction):
    def __init__(self, app, level):
        super().__init__(app)
        self.level = level

    def perform(self):
        print (f"starting new game: {self.level}")
        for newPlayer in self.app.level.entityManager.players:
            player = Player(newPlayer.controller, fg=newPlayer.fg)
            self.level.entityManager.add(player)
            player.place(self.level, self.level.map.start[0], self.level.map.start[1])

        self.app.level = self.level
        self.app.previousLevel = None