
from Components import ButtonUI, Position, Render, Selected, SliderUI, registerMenuComponents
from Levels.BaseLevel import BaseLevel
from Systems.MainMenuSystems.ButtonSystems import RenderButtonsSystem, RenderSlidersSystem, UpdateButtonsSystem
from Systems.MainMenuSystems.ChangeLevelSystem import ChangeLevelSystem


class OptionsLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        registerMenuComponents(self.e)

        centerx = int(width/2)
        centery = int(height/2)


        self.buttonsQuery = self.e.createQuery(
            allOf=[ButtonUI],
            storeQuery='Buttons'
        )
        
        self.slidersQuery = self.e.createQuery(
            allOf=[SliderUI],
            storeQuery='Sliders'
        )

        self.uiInputsQuery = self.e.createQuery(
            anyOf=[ButtonUI, SliderUI],
            storeQuery='uiInputs'
        )
        

        newGameButton = self.e.createEntity()
        self.e.addComponent(newGameButton, Position, {'x': centerx - 10, 'y': centery + 20, 'width': 10, 'height': 3})
        self.e.addComponent(newGameButton, ButtonUI, {'action': 'change_level', 'data': {'nextLevel': 'MainMenu'}})
        self.e.addComponent(newGameButton, Render, {'name': 'Back'})
        self.e.addComponent(newGameButton, Selected)

        newGameButton = self.e.createEntity()
        self.e.addComponent(newGameButton, Position, {'x': centerx - 10, 'y': centery - 20, 'width': 20, 'height': 3})
        self.e.addComponent(newGameButton, ButtonUI, {'action': 'change_tileset'})
        self.e.addComponent(newGameButton, Render, {'name': 'Choose Tiles'})

        newGameButton = self.e.createEntity()
        self.e.addComponent(newGameButton, Position, {'x': centerx - 10, 'y': centery - 15, 'width': 20, 'height': 3})
        self.e.addComponent(newGameButton, ButtonUI, {'action': 'toggle_fullscreen'})
        self.e.addComponent(newGameButton, Render, {'name': 'Toggle Fullscreen'})

        slider = self.e.createEntity()
        self.e.addComponent(slider, Position, {'x': centerx - 10, 'y': centery - 10, 'width': 40, 'height': 3})
        self.e.addComponent(slider, SliderUI)
        self.e.addComponent(slider, Render, {'name': 'Music Volume'})

        newGameButton = self.e.createEntity()
        self.e.addComponent(newGameButton, Position, {'x': centerx - 10, 'y': centery - 5, 'width': 20, 'height': 4})
        self.e.addComponent(newGameButton, ButtonUI, {'action': 'remap_controls', 'data': {'controller': 'keyboard'}})
        self.e.addComponent(newGameButton, Render, {'name': 'Remap Keyboard\nControls'})

        newGameButton = self.e.createEntity()
        self.e.addComponent(newGameButton, Position, {'x': centerx - 10, 'y': centery, 'width': 20, 'height': 4})
        self.e.addComponent(newGameButton, ButtonUI, {'action': 'remap_controls', 'data':{'controller': 'gamepad'}})
        self.e.addComponent(newGameButton, Render, {'name': 'Remap Gamepad\nControls'})
        

        # options we want in the game:
        #   choose the tileset
        #   set fullscreen or windowed?
        #   set music volume
        #   remap keyboard controls
        #   remap joystick controls




        

        self.updateButtonsSystem = UpdateButtonsSystem(self)
        self.renderButtonsSystem = RenderButtonsSystem(self)
        self.renderSlidersSystem = RenderSlidersSystem(self)
        self.changeLevelSystem = ChangeLevelSystem(self)


    def update(self):
        self.updateButtonsSystem.run()
        self.renderButtonsSystem.run()
        self.renderSlidersSystem.run()

        self.changeLevelSystem.run()