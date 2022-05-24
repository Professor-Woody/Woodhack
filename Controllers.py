import pygame
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


class KeyboardController:
    key = {}

    def setKey(self, key, state):
        self.key[key] = state

    def checkKeyPressed(self, key):
        if key not in self.key.keys():
            self.key[key] = False
            
        return self.key[key]

    def checkKeyPressedOnce(self, key):
        if key not in self.key.keys():
            self.key[key] = False

        state = self.key[key]
        self.key[key] = False
        return state

class JoystickController:
    def __init__(self, joystick):
        self.joystick = joystick
        self.actions = {
            "up": (self.getAxis, (1, -1)),
            "down": (self.getAxis, (1, 1)),
            "left": (self.getAxis, (0, -1)),
            "right": (self.getAxis, (0, 1)),
            "lefthand": (self.getAxis, (4, 1)),
            "righthand": (self.getAxis, (5, 1)),
            "use": (self.getButton, (0)),
            "cancel": (self.getButton, (1)),
            "next": (self.getButton, (4)),
            "previous": (self.getButton, (5)),
            "nearestEnemy": (self.getButton, (2)),
            "inventory": (self.getButton, (3)),
            "aimXAxis": (self.getRawAxis, (2)),
            "aimYAxis": (self.getRawAxis, (3))
        }

        self.checked = set()

    def update(self):
        if self.speed:
            self.speed -= 1
            return
        self.speed = 10

        for check in self.checked:
            command, data = self.actions[check]
            if not command(data):
                self.checked.remove(check)
        

    def getButtonForMapping(self):
        for button in range(self.joystick.get_numbuttons()):
            if self.joystick.get_button(button):
                return (self.getButton, (button))
        
        for axis in range(self.joystick.get_numaxes()):
            value = self.joystick.get_axis(axis)
            if value > .5 or value < -.5:
                return (self.getAxis, (axis, value))

        for hat in range(self.joystick.get_numhats()):
            for axis in range(2):
                value = self.joystick.get_hat(hat)[axis]
                if  value != 0:
                    return(self.getHat, (hat, axis, value))
                
    def mapButton(self, action):
        self.actions[action] = self.getButtonForMapping()


    def getButton(self, data):
        button = data[0]
        return bool(self.joystick.get_button(button))

    def getAxis(self, data):
        axis, direction = data
        if direction > 0 and self.joystick.get_axis(axis) > .5:
            return True
        if direction < 0 and self.joystick.get_axis(axis) < -.5:
            return True
        return False
            
    def getRawAxis(self, data):
        axis = data[0]
        return self.joystick.get_axis(axis)

    def getHat(self, data):
        hat, axis, direction = data
        value = self.joystick.get_hat(hat)[axis]
        if direction > 0 and value > 0:
            return True
        if direction < 0 and value < 0:
            return True
        return False           


    def getPressed(self, action):
        command, data = self.actions[action]
        return command(data)

    def getPressedOnce(self, action):
        command, data = self.actions[action]
        result = command(data)
        if result:
            self.checked.add(action)
        return result
        




