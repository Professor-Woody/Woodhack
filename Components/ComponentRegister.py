from Components.Components import *
from Components.UIComponents import *
from Components.ItemComponents import *


def registerComponents(ecs: Engine):
    components = [
        Position,
        Collision,
        Light,
        Render,
        Initiative,
        Target,
        Targeted,
        PlayerInput,
        Stats,
        IsPlayer,
        IsNPC,
        IsItem,
        IsEquipped,
        UI,
        SelectionUI,
        EffectControlsLocked,
        BlocksMovement,
        SelectionUI,
        IsEquippable,
        Body,

    ]
    for component in components:
        ecs.register_component(component)