from Systems.BaseSystem import BaseSystem



class ConsumableSystem(BaseSystem):
    actions = ['use_consumable']

    def run(self):
        # a consumable does the following:
        #   it triggers a stored action to perform an effect
        #   it destroys (or decrements) the item



        """
        Potion list
        healing
        extra healing
        full healing
        invisibility
        object detection
        enlightenment
        speed
        gain ability
        gain level
        glowing
        barkskin
        ironskin
        

        Spell list
        firebolt
        fireball
        magic mapping
        magic missile
        healing


        
        
        """