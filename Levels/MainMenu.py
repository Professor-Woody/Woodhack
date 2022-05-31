from Levels.Level import BaseLevel, GameLevel
from Actions.Actions import QuitAction
from Actions.MenuActions import ChangeLevelAction, NewGameAction
from UI import Button, Text
from Controllers import controllers
from Entity import NewPlayer



class MainMenu(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        self.app.previousLevel = self

        title = Text("Woodhack v0.0000000001")
        title.place(self, 10, 20)

        action = ChangeLevelAction(self.app, NewGameLevel(self.app, self.width, self.height))
        button = Button(" New Game ", action)
        button.place(self, 20, 40)

        action = ChangeLevelAction(self.app, OptionsLevel(self.app, self.width, self.height))
        button = Button(" Options  ", action)
        button.place(self, 20, 50)

        button = Button(" Quit     ", QuitAction())
        button.place(self, 20, 60)
        print (f"mainmenu {self.entityManager}")


class OptionsLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        title = Text("Options Menu")
        title.place(self, 10, 20)

        action = ChangeLevelAction(self.app, self.app.previousLevel)
        button = Button(" Go Back ", action)
        button.place(self, 20, 60)

        print (f"options menu {self.entityManager}")



class NewGameLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        title = Text("New Game")
        title.place(self, 10, 20)

        title = Text("Players:")
        title.place(self, 20, 40)

        self.unassignedControllers = controllers.copy()


    def update(self):
        # check if any unmapped controllers have pressed the use button
        # if so then map them to a player.
        for controller in self.unassignedControllers:
            controller.update()
            if controller.getPressedOnce("use"):
                # create a new player object
                player = NewPlayer(controller)
                x = (len(self.entityManager.players) * 20) + 20
                player.place(self, x, 60)
                self.unassignedControllers.remove(controller)

        count = 0        
        for player in self.entityManager.players:
            if player.ready:
                count += 1
        if count and count == len(self.entityManager.players):
            level = GameLevel(self.app, self.width, self.height)
            NewGameAction(self.app, level).perform()

        self.entityManager.update()
