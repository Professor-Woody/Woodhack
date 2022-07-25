
from Components import ButtonUI, Position, Render, registerMenuComponents
from Levels.BaseLevel import BaseLevel
from Systems.ButtonSystems import RenderButtonsSystem, UpdateButtonsSystem
from Systems.ChangeLevelSystem import ChangeLevelSystem


class OptionsLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        registerMenuComponents(self.e)

        centerx = int(width/2)
        centery = int(height/2)

        
        newGameButton = self.e.createEntity()
        self.e.addComponent(newGameButton, Position, {'x': centerx - 5, 'y': centery + 20, 'width': 10, 'height': 5})
        self.e.addComponent(newGameButton, ButtonUI, {'action': 'change_level', 'data': {'nextLevel': 'MainMenu'}, 'selected': True})
        self.e.addComponent(newGameButton, Render, {'name': 'Back'})

        self.buttonsQuery = self.e.createQuery(
            allOf=[ButtonUI],
            storeQuery='Buttons'
        )

        self.updateButtonsSystem = UpdateButtonsSystem(self)
        self.renderButtonsSystem = RenderButtonsSystem(self)
        self.changeLevelSystem = ChangeLevelSystem(self)


    def update(self):
        self.updateButtonsSystem.run()
        self.renderButtonsSystem.run()

        self.changeLevelSystem.run()