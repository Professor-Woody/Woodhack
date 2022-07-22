from Systems.BaseSystem import BaseSystem
from Components import *
import Helpers.PositionHelper as PositionHelper
import tcod
import numpy as np

class AISystem(BaseSystem):
    def run(self):
        # the standard hostile AI should do the following:
            # if no enemies and no path, sit still and wait
            # if enemies and no target, choose a target
                # if a target, path to it and move
                # every 4 seconds confirm they're still the closest target

        npcs = self.level.npcsQuery.result
        if npcs:
            targetComponents = self.getComponents(Target)
            aiComponents = self.getComponents(AI)
            positionComponents = self.getComponents(Position)
            statsComponents = self.getComponents(Stats)
            bodyComponents = self.getComponents(Body)

        for entity in npcs:
            aiComponents[entity]['targetRefreshTimer'] -= 1
            if aiComponents[entity]['targetRefreshTimer'] <= 0:
                aiComponents[entity]['targetRefreshTimer'] = 120
                self.recheckTargets(entity, targetComponents, positionComponents)

            if self.level.e.hasComponent(entity, IsReady):
                if not targetComponents[entity]['target']:
                    self.level.post('add_speed', {'entity': entity, 'speed': 125})
                    continue

                target = targetComponents[entity]['target']


                distance = PositionHelper.getRange(
                    (positionComponents[entity]['x'], positionComponents[entity]['y']),
                    (positionComponents[target]['x'], positionComponents[target]['y'])
                ) 
                if distance > 1:
                    if distance < 5 or not aiComponents[entity]['path']:
                        aiComponents[entity]['path'] = self.getPathTo(entity, target, positionComponents)

                    if aiComponents[entity]['path']:
                        # This little bit protects against the previous move being blocked
                        if aiComponents[entity]['path'][0][0] == positionComponents[entity]['x'] and \
                        aiComponents[entity]['path'][0][1] == positionComponents[entity]['y']:
                            aiComponents[entity]['path'].pop(0)

                        if not aiComponents[entity]['path']:
                            # we've run out of path but our target has moved
                            aiComponents[entity]['targetRefreshTimer'] = 0
                            continue


                        nextStep = aiComponents[entity]['path'][0]
                        dx = nextStep[0] - positionComponents[entity]['x']
                        dy = nextStep[1] - positionComponents[entity]['y']
                        self.level.post('move', {'entity': entity, 'dx': dx, 'dy': dy})
                        self.level.post('add_speed', {'entity': entity, 'speed': statsComponents[entity]['moveSpeed']})
                        continue
                
                else:
                    if not bodyComponents[entity]['mainhand']:
                        self.level.post('add_speed', {'entity': entity, 'speed': 180})
                        continue

                    if self.level.e.hasComponent(bodyComponents[entity]['mainhand'], IsReady):
                        self.level.post('melee', {'slot': 'mainhand', 'target': target, 'entity': entity, 'item': bodyComponents[entity]['mainhand']})
                        continue





    def recheckTargets(self, entity, targetComponents, positionComponents):
        currentTarget = targetComponents[entity]['target']
        if currentTarget:
            # if we can see the current target do nothing
            if PositionHelper.getLOS(
            (positionComponents[entity]['x'], positionComponents[entity]['y']),
            (positionComponents[currentTarget]['x'], positionComponents[currentTarget]['y']),
            20,
            self.level.map):
                return

        targets = []
        for target in self.level.playersQuery.result:
            los = PositionHelper.getLOS(
            (positionComponents[entity]['x'], positionComponents[entity]['y']),
            (positionComponents[target]['x'], positionComponents[target]['y']),
            20,
            self.level.map)
            if los:
                targets.append((target, len(los)-1))
        
        if targets:
            targets.sort(key = lambda x: x[1])
            targetComponents[entity]['target'] = targets[0][0]




    def getPathTo(self, entity, target, positionComponents):
        dx = positionComponents[target]['x']
        dy = positionComponents[target]['y']


        cost = np.array(self.level.map.tiles["passable"], dtype=np.int8)
        for actor in self.level.collidableQuery.result: #TODO: Replace this query with a collideable one
            if actor != entity and cost[positionComponents[actor]['x'], positionComponents[actor]['y']]:
                # add to cost of a blocked position
                # there's a potential for the entity to move out so we still
                # count it as a possible path.

                # a lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player
                cost[positionComponents[actor]['x'], positionComponents[actor]['y']] += 10
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)
        pathfinder.add_root((positionComponents[entity]['x'], positionComponents[entity]['y']))
        path = pathfinder.path_to((dx, dy))[1:].tolist()
        result = [(index[0], index[1]) for index in path]
        return result
                    

