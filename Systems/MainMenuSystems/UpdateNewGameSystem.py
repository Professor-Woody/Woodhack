from Components import Parent, PlayerInput, Render, Stat, Stats
from Levels.BaseLevel import TestLevel
from Systems.BaseSystem import BaseSystem
import copy


class UpdateNewGameSystem(BaseSystem):
    actions = ['player_ready']
    alwaysActive=False
    priority=120

    def run(self):
        if self._actionQueue:
            unreadyPlayers = self.level.claimedPanesQuery.result
            readyPlayers = self.level.readyPlayersQuery.result
            print ("in newgamesystem")
            print (readyPlayers)
            print (unreadyPlayers)

            if readyPlayers and not unreadyPlayers:
                print ("All players ready!")
                # all loaded players are ready
                oldInputComponents = self.getComponents(PlayerInput)
                oldRenderComponents = self.getComponents(Render)

                newLevel = TestLevel(self.level.app, self.level.width, self.level.height)
                statsComponents = newLevel.e.component.components[Stats]
                renderComponents = newLevel.e.component.components[Render]


                stats = ['str', 'dex', 'int', 'con']

                for player in readyPlayers:
                    entity = newLevel.e.spawn("PLAYER",  newLevel.map.startPoint[0], newLevel.map.startPoint[1])
                    newLevel.e.addComponent(entity, PlayerInput, {'controller': oldInputComponents[player]['controller']})

                    # add starter equipment based on class

                    # add stats from controls into stats
                    for stat in stats:
                        statValue = self.getStat(stat, player)
                        statsComponents[entity][stat] = statValue
                        if stat == 'con':
                            statsComponents[entity]['hpLevelHistory'].append(statValue)
                    
                    # add colour to render
                    renderComponents[entity]['fg'] = oldRenderComponents[player]['fg']
                    
                    # add name to render
                    renderComponents[entity]['name'] = oldRenderComponents[player]['name']

                    newLevel.post('recalculate_stats', {'entity': entity})

                self.level.app.level = newLevel


    def getStat(self, name, player):
        entities = self.level.statDisplayQuery.result
        parentComponents = self.getComponents(Parent)
        statComponents = self.getComponents(Stat)

        for entity in entities:
            if parentComponents[entity]['entity'] == player:
                if statComponents[entity]['name'] == name:
                    return statComponents[entity]['value']