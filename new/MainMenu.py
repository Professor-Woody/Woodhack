from Level import BaseLevel
from Actions import PrintAction
from UI import Button, Text
from Controllers import controllers


class MainMenu(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        title = Text("Woodhack v0.0000000001")
        title.place(10, 20)

        action = ChangeLevelAction(self.app, NewGameLevel(self.app, self.width, self.height))
        button = Button(" New Game ", action)
        button.place(self, 20, 20)

        action = ChangeLevelAction(self.app, OptionsLevel(self.app, self.width, self.height))
        button = Button(" Options  ", action)
        button.place(self, 20, 40)

        button = Button(" Quit     ", QuitAction())
        button.place(self, 20, 60)


class OptionsLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        title = Text("Options Menu")
        title.place(10, 20)

        action = ChangeLevelAction(self.app, self.app.previousLevel)
        button = Button(" Go Back ", action)
        button.place(self, 20, 40)

        self.unassignedControllers = controllers.copy()



class NewGameLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        title = Text("New Game")
        title.place(10, 20)

        title = Text("Players:")
        title.place(20, 40)


    def update(self):
        # check if any unmapped controllers have pressed the use button
        # if so then map them to a player.
        for controller in self.unassignedControllers:
            controller.update()
            if controller.getPressed("use"):
                # create a new player object
                player = NewPlayer(controller)
                x = (len(self.entityManager.players) * 20) + 20
                player.place(self, x, 60)
                self.unassignedControllers.remove(controller)

        count = 0        
        for player in self.entityManager.players:
            if player.ready:
                count += 1
        if count == len(self.entityManager.players):
            level = GameLevel(self.app, self.width, self.height)
            ChangeLevelAction(self.app, level).perform()

        self.entityManager.update()
