from Components import IsActive, PlayerInput, Parent
from Systems.BaseSystem import BaseSystem


class CheckControllersSystem(BaseSystem):

    def run(self):
        if self.level.controllers:
            parentComponents = self.getComponents(Parent)
            for controller in self.level.controllers:
                controller.update()
                if controller.getPressedOnce('use'):
                    print (f"{controller} pressed")
                    # player activated.  Assign controller to player and 
                    # remove from list
                    entity = self.level.players.pop()
                    self.level.e.addComponent(entity, PlayerInput, {'controller': controller})
                    self.level.e.addComponent(entity, IsActive)
                    for ui in self.level.childEntitiesQuery.result:
                        if parentComponents[ui]['entity'] == entity:
                            self.level.e.addComponent(ui, IsActive)
                    self.level.controllers.remove(controller)
                    self.level.app.screen.clear()