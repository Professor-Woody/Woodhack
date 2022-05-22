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
    actions = {
        "up": False,
        "down": False,
        "left": False,
        "right": False,
        "lefthand": False,
        "righthand": False,
        "use": False,
        "cancel": False,
        "next": False,
        "previous": False,
        "nearestEnemy": False,
        "inventory": False
    }

    mappings = {
        0: "use",
        1: "cancel",
        2: "nearestEnemy",
        3: "inventory",
        4: "previous",
        5: "next",
        "dpad-left": "left",
        "dpad-right": "right",
        "dpad-up": "up",
        "dpad-down": "down",
        "l-trigger": "lefthand",
        "r-trigger": "righthand"
    }

    def __init__(self, joystick):
        self.joystick = joystick

    def update(self):
        for button in self.joystick.get_numbuttons():
            if button in self.actions.keys():
                self.actions[button]=self.joystick.get_button(button)
        

