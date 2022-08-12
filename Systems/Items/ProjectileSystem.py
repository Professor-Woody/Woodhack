from Systems.BaseSystem import BaseSystem
from Components import Parent, Projectile, Position, Stats, WeaponStats
from random import randint
import Colours as colour

class UpdateProjectilesSystem(BaseSystem):
    priority=170

    def run(self):
        entities = self.level.projectilesQuery.result
        projectileComponents = self.getComponents(Projectile)
        positionComponents = self.getComponents(Position)
        statsComponents = self.getComponents(Stats)
        weaponComponents = self.getComponents(WeaponStats)

        for entity in entities:
            # if path
            if projectileComponents[entity]['path']:
                print (f"{entity} has path {projectileComponents[entity]['path']}")
                nextSpace = projectileComponents[entity]['path'].pop(0)
                blocked = self.level.map.checkIsBlocked(nextSpace[0], nextSpace[1])
                # check next space
                if blocked:
                    print (f"blocked: {blocked}")
                    if self.hasComponent(blocked, projectileComponents[entity]['targetType']):
                    # if targetType, apply damage
                        attackRoll = randint(-9, 10) + projectileComponents[entity]['attack'] - statsComponents[blocked]['defence']
                        print ("attacky")
                        if attackRoll >= 0:
                            damageRoll = sum([randint(1, weaponComponents[entity]['damageDiceType']) for dice in range(weaponComponents[entity]['damageDiceAmount'])]) \
                                + weaponComponents[entity]['damageBonus'] \
                                    + projectileComponents[entity]['damageBonus']
                            self.level.post('damage', {'entity': blocked, 'damage': damageRoll})
                            self.level.post('create_effect', {
                                "type": "label",
                                "x": positionComponents[entity]['x'] -1,
                                "y": positionComponents[entity]['y'] -1,
                                "name": f"┤{damageRoll}├",
                                "fg": colour.RED
                            })
                            self.removeProjectile(entity)
                    # else:
                    #     print (f"blocked by something else: {blocked}")
                    #     self.removeProjectile(entity)
                else:
                    if self.level.map.checkIsPassable(nextSpace[0], nextSpace[1]):
                        print ("moving")
                        positionComponents[entity]['x'] = nextSpace[0]
                        positionComponents[entity]['y'] = nextSpace[1]
                        self.level.post('add_speed', {'entity': entity, 'speed': projectileComponents[entity]['speed']})
                    else:
                        print ("not passable")
                        self.removeProjectile(entity)
            else:
                self.removeProjectile(entity)
    
    def removeProjectile(self, entity):
        self.level.e.removeComponent(entity, Projectile)
        self.level.e.removeComponent(entity, Parent) # don't need this anymore
    # else just stop and drop projectile there for now (will free fly it later)
        