import pygame
pygame.joystick.init()
import tcod

class BaseController:
    pass

class JoystickController(BaseController):
    parent = None
    
    def __init__(self, joystick):
        self.joystick = joystick
        self.commands = {
            "up": (self.getAxis, (1, -1)),
            "down": (self.getAxis, (1, 1)),
            "left": (self.getAxis, (0, -1)),
            "right": (self.getAxis, (0, 1)),
            "lefthand": (self.getAxis, (4, 1)),
            "righthand": (self.getAxis, (5, 1)),
            "use": (self.getButton, [0]),
            "cancel": (self.getButton, [1]),
            "next": (self.getButton, [5]),
            "previous": (self.getButton, [4]),
            "nearestEnemy": (self.getButton, [2]),
            "inventory": (self.getButton, [3]),
            "aimXAxis": (self.getRawAxis, [2]),
            "aimYAxis": (self.getRawAxis, [3])
        }

        self.checked = []

    def update(self):
        for check in self.checked:
            command, data = self.commands[check]
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
                
    def mapButton(self, command):
        self.commands[command] = self.getButtonForMapping()


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


    def getPressed(self, cmd):
        command, data = self.commands[cmd]
        return command(data)

    def getPressedOnce(self, cmd):
        command, data = self.commands[cmd]
        result = command(data)
        if result and cmd not in self.checked:
            self.checked.append(cmd)
            return True
        return False
        
controllers = [JoystickController(pygame.joystick.Joystick(x)) for x in range(pygame.joystick.get_count())]