from Components import EntityInfo, InfoPanel, IsActive, Parent, Position, Render, Target
from Systems.BaseSystem import BaseSystem
import Colours as colour




class CloseInfoPanelsSystem(BaseSystem):
    actions = ['close_info_panel']
    priority=30

    def run(self):
        if self._actionQueue:

            for action in self.actionQueue:
                entity = action['entity']
                self.level.e.removeComponent(entity, IsActive)




class RenderInfoPanelsSystem(BaseSystem):
    priority=110
    
    def run(self):
        positionComponents = self.getComponents(Position)
        renderComponents = self.getComponents(Render)
        targetComponents = self.getComponents(Target)
        infoComponents = self.getComponents(EntityInfo)
        parentComponents = self.getComponents(Parent)

        screen = self.level.app.screen

        for entity in self.level.activePanelsQuery.result:
            parentEntity = parentComponents[entity]['entity']
            subject = targetComponents[entity]['target']
            # print (infoComponents)
            if subject and self.level.e.hasComponent(subject, EntityInfo):
            # draw the frame
                screen.drawFrame(
                    positionComponents[entity]['x'],
                    positionComponents[entity]['y'],
                    positionComponents[entity]['width'],
                    positionComponents[entity]['height'],
                    # renderComponents[entity]['name'],
                    fg=renderComponents[parentEntity]['fg']
                )
            # draw the image
                height = 0
                if infoComponents[subject]['image']:
                    screen.printLines(
                        positionComponents[entity]['x']+2,
                        positionComponents[entity]['y']+2,
                        infoComponents[subject]['image']
                    )
                    height = len(infoComponents[subject]['image'].split('\n')) + 1
                # draw the primary text

                if infoComponents[subject]['primaryText']:
                    screen.printLines(
                        positionComponents[entity]['x']+16,
                        positionComponents[entity]['y']+2,
                        infoComponents[subject]['primaryText']
                    )
                    tempHeight = len(infoComponents[subject]['primaryText'].split('\n')) + 1
                    if tempHeight > height:
                        height = tempHeight

                # draw the secondary text
                if infoComponents[subject]['secondaryText']:
                    screen.printLines(
                        positionComponents[entity]['x']+2,
                        positionComponents[entity]['y']+2 + height,
                        infoComponents[subject]['secondaryText']
                    )
"""

o=(===>

o={======>

        _____
        \   /
=I======|===|D
        /___\ 
      



"""