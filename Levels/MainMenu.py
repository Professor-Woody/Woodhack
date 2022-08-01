

from Components import ButtonUI, Position, Render, Selected, SliderUI, registerMenuComponents
from Levels.BaseLevel import BaseLevel
from Systems.MainMenuSystems.ButtonSystems import RenderButtonsSystem, UpdateButtonsSystem
from Systems.MainMenuSystems.ChangeLevelSystem import ChangeLevelSystem
from Systems.LevelSystems.QuitSystems import QuitSystem


class MainMenu(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        registerMenuComponents(self.e)

        centerx = int(width/2) - 10
        centery = int(height/2)

        newGameButton = self.e.createEntity()
        self.e.addComponent(newGameButton, Position, {'x': centerx, 'y': centery, 'width': 20, 'height': 5})
        self.e.addComponent(newGameButton, ButtonUI, {'action': 'change_level', 'data': {'nextLevel': 'CharacterSelect'}})
        self.e.addComponent(newGameButton, Render, {'name': 'New Game'})
        self.e.addComponent(newGameButton, Selected)

        # newGameButton = self.e.createEntity()
        # self.e.addComponent(newGameButton, Position, {'x': centerx, 'y': centery + 10, 'width': 20, 'height': 5})
        # self.e.addComponent(newGameButton, ButtonUI, {'action': 'load ButtonClicked'})
        # self.e.addComponent(newGameButton, Render, {'name': 'Load Game'})

        newGameButton = self.e.createEntity()
        self.e.addComponent(newGameButton, Position, {'x': centerx, 'y': centery + 10, 'width': 20, 'height': 5})
        self.e.addComponent(newGameButton, ButtonUI, {'action': 'change_level', 'data': {'nextLevel': 'Options'}})
        self.e.addComponent(newGameButton, Render, {'name': 'Options'})        

        newGameButton = self.e.createEntity()
        self.e.addComponent(newGameButton, Position, {'x': centerx, 'y': centery + 20, 'width': 20, 'height': 5})
        self.e.addComponent(newGameButton, ButtonUI, {'action': 'quit'})
        self.e.addComponent(newGameButton, Render, {'name': 'Quit'})

        self.buttonsQuery = self.e.createQuery(
            allOf=[ButtonUI],
            storeQuery='Buttons'
        )
        self.uiInputsQuery = self.e.createQuery(
            anyOf=[ButtonUI, SliderUI],
            storeQuery='uiInputs'
        )

        self.updateButtonsSystem = UpdateButtonsSystem(self)
        self.renderButtonsSystem = RenderButtonsSystem(self)
        self.changeLevelSystem = ChangeLevelSystem(self)
        self.quitSystem = QuitSystem(self)

    def update(self):
        self.runSystems()
        # self.updateButtonsSystem.run()
        # self.renderButtonsSystem.run()

        # self.changeLevelSystem.run()
        # self.quitSystem.run()