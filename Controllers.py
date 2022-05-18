from Events import KeyDownEvent, KeyUpEvent

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