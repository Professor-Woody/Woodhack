from Actions.EffectsActions import RecalculateStatsAction
from Components.Components import Light, Body

class SubSystem:
    def __init__(self, system):
        system.register(RecalculateStatsAction, self)

    def run(self, action):
        print ("new new recalculating stats")

        # recalculating light
        action.entity[Light].radius = action.entity[Light].baseRadius
        
        for key in action.entity[Body].slots.keys():
            slot = action.entity[Body].slots[key]
            print (key, slot)
            if slot and slot.has(Light) and slot[Light].radius > action.entity[Light].radius:
                action.entity[Light].radius = slot[Light].radius
                print (f"new light radius: {action.entity[Light].radius}")
                