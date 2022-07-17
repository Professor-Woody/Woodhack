componentMap = {
    'Position': 1,
    'Render': 2,
    'Light': 3,
    'IsPlayer': 4,
    'IsNPC': 5,
    'IsItem': 6,
    'IsVisible': 7,
    'PlayerInput': 8,
    'IsReady': 9,
    'Init': 10, 
    'Target': 11,
    'Targeted': 12
}

def registerComponents(entityManager):
    entityManager.registerComponent(Position, {'x': 0, 'y': 0})
    entityManager.registerComponent(Render, {'char': '@', 'name': 'Woody', 'fg': (255, 0,0), 'bg': None})
    entityManager.registerComponent(Light, {'radius': 3})
    entityManager.registerComponent(IsPlayer)
    entityManager.registerComponent(IsNPC)
    entityManager.registerComponent(IsItem)
    entityManager.registerComponent(IsVisible)
    entityManager.registerComponent(PlayerInput, {'controller': None})
    entityManager.registerComponent(IsReady)
    entityManager.registerComponent(Init, {'speed': 0})
    entityManager.registerComponent(Target, {'target': None})
    entityManager.registerComponent(Targeted, {'targetedBy': [], 'targetTimer': 0, 'targetIndex': 0})

Position = 1
Render = 2
Light = 3
IsPlayer = 4
IsNPC = 5
IsItem = 6
IsVisible = 7
PlayerInput = 8
IsReady = 9
Init = 10
Target = 11
Targeted = 12


