from Components import IsNPC, IsReady, Parent, Position, Projectile, Ranged, Render, Stats, Target, WeaponStats
from Systems.BaseSystem import BaseSystem
import Helpers.PositionHelper as PositionHelper

class RangedSystem(BaseSystem):
    actions=['use_ranged']

    def run(self):
        if self._actionQueue:
            renderComponents = self.getComponents(Render)
            positionComponents = self.getComponents(Position)
            targetComponents = self.getComponents(Target)
            rangedComponents = self.getComponents(Ranged)
            statsComponents = self.getComponents(Stats)
            weaponComponents = self.getComponents(WeaponStats)

            for action in self.actionQueue:
                # check we are ready
                entity = action['entity']
                parent = action['parentEntity']

                if self.hasComponent(entity, IsReady):
                    # check we have ammo
                    # we'll ignore this for now
                    if True:
                        # check we have a target
                        target = targetComponents[parent]['target']
                        if target:
                            # check we have LOS 
                            # TODO: OR! shoot along the targeting line (twin stick/mouse)

                            los = PositionHelper.getLOS(
                                (positionComponents[parent]['x'], positionComponents[parent]['y']),
                                (positionComponents[target]['x'], positionComponents[target]['y']),
                                100,
                                self.level.map
                            )
                            if los:
                                rise = positionComponents[target]['y'] - positionComponents[parent]['y']
                                run = positionComponents[target]['x'] - positionComponents[parent]['x']

                                # create projectile from ammo. For the moment lets just make a basic arrow
                                projectile = self.level.e.spawn('arrow', positionComponents[parent]['x'], positionComponents[parent]['y'])
                                self.level.e.addComponent(projectile, Parent, {'entity': parent})
                                self.level.e.addComponent(projectile, Projectile, {
                                    'rise': rise,
                                    'run': run,
                                    'path': los,
                                    'speed': 1,
                                    'targetType': IsNPC,
                                    'attack': rangedComponents[entity]['attack'] + statsComponents[parent]['attack'] + statsComponents[parent]['dex'],
                                    'damageBonus': 0
                                })
                                self.clog("Twang!", renderComponents[parent]['fg'])
                                self.level.post('add_speed', {'entity': parent, 'speed': weaponComponents[entity]['moveSpeed']})
                                self.level.post('add_speed', {'entity': entity, 'speed': weaponComponents[entity]['weaponSpeed']})



                    else:
                        self.log(f"£{parent}$ can't use £{entity}$: No ammo")

                # subtract ammo
                # create projectile
                # post everything
                print (f"Ranged action: {action}")