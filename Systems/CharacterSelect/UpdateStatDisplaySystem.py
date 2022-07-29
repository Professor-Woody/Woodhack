from Components import Parent, Stat, StatPoints
from Systems.BaseSystem import BaseSystem



class UpdateStatDisplaySystem(BaseSystem):
    actions=['toggle_stat']

    def run(self):
        if self._actionQueue:
            statComponents = self.getComponents(Stat)
            pointsComponents = self.getComponents(StatPoints)
            parentComponents = self.getComponents(Parent)

            for action in self.actionQueue:
                # find the stat in the pane that's being updated

                pane = action['entity']
                name = action['selection']
                command = action['command']

                entity = None
                for ui in self.level.childEntitiesQuery.result:
                    if parentComponents[ui]['entity'] == pane \
                        and self.level.e.hasComponent(ui, Stat) \
                            and statComponents[ui]['name'] == name:
                        entity = ui
                        break
                
                if entity:
                    # update the stat
                    if command == 'left':
                        if statComponents[entity]['value'] > statComponents[entity]['baseValue']:
                            statComponents[entity]['value'] -= 1
                            pointsComponents[pane]['value'] += 1
                    else:
                        if pointsComponents[pane]['value'] > 0:
                            statComponents[entity]['value'] += 1
                            pointsComponents[pane]['value'] -= 1
                    print (f"setting stat {pane}:{name} to {statComponents[entity]['value']}.  {pointsComponents[pane]['value']} points left")
