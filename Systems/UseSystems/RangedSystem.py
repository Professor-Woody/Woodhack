from Components import Body, Equipped, Inventory, IsNPC, IsPlayer, IsReady, Parent, PlayerInput, Position, Projectile, Ranged, Render, Stackable, Stats, Target, Type, WeaponStats
from Systems.BaseSystem import BaseSystem
import Helpers.PositionHelper as PositionHelper

class RangedSystem(BaseSystem):
    actions=['use_ranged']
    alwaysActive=False
    priority=160

    def run(self):
        if self._actionQueue:
            renderComponents = self.getComponents(Render)
            positionComponents = self.getComponents(Position)
            targetComponents = self.getComponents(Target)
            rangedComponents = self.getComponents(Ranged)
            statsComponents = self.getComponents(Stats)
            weaponComponents = self.getComponents(WeaponStats)
            bodyComponents = self.getComponents(Body)
            typeComponents = self.getComponents(Type)
            quantityComponents = self.getComponents(Stackable)
            inventoryComponents = self.getComponents(Inventory)
            inputComponents = self.getComponents(PlayerInput)


            for action in self.actionQueue:
                # check we are ready
                entity = action['entity']
                parent = action['parentEntity']

                if self.hasComponent(entity, IsReady):
                    # check we have ammo)
                    if bodyComponents[parent]['offhand'] and \
                            typeComponents[bodyComponents[parent]['offhand']]['primary'] == rangedComponents[entity]['ammoType']:
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
                            if los and self.level.map.checkIsVisible(positionComponents[target]['x'], positionComponents[target]['y']):
                                rise = positionComponents[target]['y'] - positionComponents[parent]['y']
                                run = positionComponents[target]['x'] - positionComponents[parent]['x']

                                # create projectile from ammo. For the moment lets just make a basic arrow
                                if quantityComponents[bodyComponents[parent]['offhand']]['quantity'] == 1:
                                    projectile = bodyComponents[parent]['offhand']
                                    self.level.e.addComponent(projectile, Position, {'x': positionComponents[parent]['x'], 'y': positionComponents[parent]['y']})
                                    bodyComponents[parent]['offhand'] = None
                                    inventoryComponents[parent]['contents'].remove(projectile)
                                    self.level.e.removeComponent(projectile, Equipped)
                                else:
                                    projectile = self.level.e.spawn('arrow', positionComponents[parent]['x'], positionComponents[parent]['y'])
                                    quantityComponents[projectile]['quantity'] = 1
                                    quantityComponents[bodyComponents[parent]['offhand']]['quantity'] -= 1

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
                                if self.hasComponent(parent, IsPlayer):
                                    self.clog("Twang!", renderComponents[parent]['fg'])
                                self.level.post('add_speed', {'entity': parent, 'speed': weaponComponents[entity]['moveSpeed']})
                                self.level.post('add_speed', {'entity': entity, 'speed': weaponComponents[entity]['weaponSpeed']})
                            else:
                                if self.hasComponent(parent, IsPlayer):
                                    self.log(f"£{parent}$ has cannot see target")
                                    inputComponents[parent]['controller'].lock(action['command'])
                        else:
                            if self.hasComponent(parent, IsPlayer):
                                self.log(f"£{parent}$ has no target")
                                inputComponents[parent]['controller'].lock(action['command'])

                    else:
                        if self.hasComponent(parent, IsPlayer):
                            self.log(f"£{parent}$ can't use £{entity}$: No ammo")

