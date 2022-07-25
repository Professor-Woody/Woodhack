import Colours as colour

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
    'Targeted': 12,
    'Inventory': 13,
    'SelectionUI': 14,
    'Body': 15,
    'Equip': 16,
    'Equipped': 17,
    'Stats': 18,
    'StatModifier': 19,
    'Melee': 20,
    'HostileAI': 21,
    'AI': 22,
    'Collidable': 23,
    'PlayerUI': 24
}

def registerComponents(entityManager):
    entityManager.registerComponent(Position, {'x': 0, 'y': 0, 'width': 1, 'height': 1, 'moveSpeed': 6})
    entityManager.registerComponent(Render, {'char': '@', 'name': 'Woody', 'fg': (255, 0,0), 'bg': None})
    entityManager.registerComponent(Light, {'radius': 1})
    entityManager.registerComponent(IsPlayer, {'id': 0})
    entityManager.registerComponent(IsNPC)
    entityManager.registerComponent(IsItem)
    entityManager.registerComponent(IsVisible)
    entityManager.registerComponent(PlayerInput, {'controller': None, 'controlFocus': []})
    entityManager.registerComponent(IsReady)
    entityManager.registerComponent(Init, {'speed': 0, 'maxSpeed': 0})
    entityManager.registerComponent(Target, {'target': None})
    entityManager.registerComponent(Targeted, {'targetedBy': [], 'targetTimer': 0, 'targetIndex': 0})
    entityManager.registerComponent(Inventory, {'contents': []})
    entityManager.registerComponent(SelectionUI, {'items': [], 'title': 'selectionUI', 'selectionIndex': 0, 'fg': colour.WHITE, 'bg': colour.BLACK})
    entityManager.registerComponent(Body, {
        'mainhand': None,
        'offhand': None,
        'head': None,
        'chest': None,
        'legs': None,
        'feet': None,
        })
    entityManager.registerComponent(Equip, {'slots': ['mainhand']})
    entityManager.registerComponent(Equipped, {'slot': "NOTEQUIPPED"})
    entityManager.registerComponent(Stats, {
        'hp': 10,
        'maxHp': 10,
        'baseMaxHp': 10,
        'attack': 0,
        'baseAttack': 0,
        'defence': 0,
        'baseDefence': 0,
        'moveSpeed': 10,
        'baseMoveSpeed': 14
        })
    entityManager.registerComponent(StatModifier)
    entityManager.registerComponent(Melee, {
        'range': 1,
        'moveSpeed': 30,
        'weaponSpeed': 60,
        'attack': 0,
        'damageBonus': 0,
        'damageDiceAmount': 1,
        'damageDiceType': 6,
    })
    entityManager.registerComponent(HostileAI, {
        'targetCooldown': 0,

    })
    entityManager.registerComponent(AI, {
        'targetRefreshTimer': 0,
        'path': []
    }),
    entityManager.registerComponent(Collidable)
    entityManager.registerComponent(PlayerUI, {
        'update': False
    })

def registerMenuComponents(entityManager):
    entityManager.registerComponent(Position, {'x': 0, 'y': 0, 'width': 1, 'height': 1, 'moveSpeed': 6})
    entityManager.registerComponent(Render, {'char': '@', 'name': 'Woody', 'fg': (255, 0,0), 'bg': None})
    entityManager.registerComponent(ButtonUI, {'selected': False, 'action': 'ButtonClickedNothing', 'data': {}})

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
Inventory = 13
SelectionUI = 14
Body = 15
Equip = 16
Equipped = 17
Stats = 18
StatModifier = 19
Melee = 20
HostileAI = 21
AI = 22
Collidable = 23
PlayerUI = 24
ButtonUI = 25