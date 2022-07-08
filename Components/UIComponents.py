from ecstremity import Component
from Components.PlayerInputComponents import PlayerInput

class SelectionUI(Component):
    def __init__(self, parentEntity, selectionList, commands):
        self.selectionIndex = 0
        self.parentEntity = parentEntity
        self.selectionList = selectionList
        # format for commands:
        # ['eventname', {'data': ....}]
        self.commands = commands



    def on_update(self, action):
        # if not self.parentEntity[PlayerInput].controlFocus:
        #     self.entity.destroy()
        if self.entity != self.parentEntity[PlayerInput].controlFocus[-1]:
            return
        dy = 0
        if self.parentEntity[PlayerInput].controller.getPressedOnce('up'):
            dy -= 1
        elif self.parentEntity[PlayerInput].controller.getPressedOnce('down'):
            dy += 1

        self.selectionIndex += dy
        if self.selectionIndex < 0:
            self.selectionIndex = len(self.selectionList)-1
        elif self.selectionIndex >= len(self.selectionList):
            self.selectionIndex = 0        
        print ('closing')
        for command in self.commands.keys():
            print (2)
            if self.parentEntity[PlayerInput].controller.getPressedOnce(command):
                print (3)
                self.parentEntity.fire_event(self.commands[command][0], self.commands[command][1])
                print (4)

    def on_close_UI(self, action):
        print ('closing')
        self.parentEntity[PlayerInput].controlFocus.remove(self.entity)
        print (2)
        self.entity.destroy()
        print (3)