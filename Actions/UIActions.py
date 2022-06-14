from Actions.BaseActions import EntityAction


class GetSelectionInputAction(EntityAction):
    def perform(self):
        dy = 0
        if self.entity['SelectionUI'].parentEntity['PlayerInput'].controller.getPressedOnce("up"):
            dy -= 1
        if self.entity['SelectionUI'].parentEntity['PlayerInput'].controller.getPressedOnce("down"):
            dy += 1
        if dy:
            self.entity['SelectionUI'].choice += dy
            if self.entity['SelectionUI'].choice < 0:
                self.entity['SelectionUI'].choice = len(self.entity['SelectionUI'].items)-1
            elif self.entity['SelectionUI'].choice >= len(self.entity['SelectionUI'].items):
                self.entity['SelectionUI'].choice = 0

        for action in self.entity['SelectionUI'].actions.keys():
            if self.entity['SelectionUI'].parentEntity['PlayerInput'].controller.getPressedOnce(action):
                self.entity['SelectionUI'].parentEntity.remove('EffectControlsLocked')
                self.entity['SelectionUI'].actions[action].perform()
                break
                

class CancelSelectionUIAction(EntityAction):
    def perform(self):
        print ("cancelling (no action)")
        DestroyUIAction(self.entity).perform()



class DestroyUIAction(EntityAction):
    def perform(self):
        if self.entity.has('UI'):
            self.entity.destroy()
        else:
            print (f"!!!!! Why are you trying to destroy {self.entity} !!!!!")