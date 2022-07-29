from EntityManager import EntityManager, Position, Render
from Levels.LevelCreator import LevelCreator
from Components import *
from Systems.AISystem import AISystem
from Systems.BaseSystem import BaseSystem
from Systems.InitSystem import InitSystem
from Systems.MeleeSystem import DamageSystem, DeathSystem, MeleeSystem
from Systems.MessageLogSystem import CombatLogSystem, MessageLogSystem
from Systems.MoveSystem import MoveSystem
from Systems.PlayerInputSystem import PlayerInputSystem
from Systems.RenderSystems import CloseUISystem, RenderEntitiesSystem, RenderPlayerUISystem, RenderSelectionUISystem, UpdateSelectionUISystem
from Systems.InventorySystem import *
from Controllers import controllers
import time
from Systems.StatsSystem import RecalculateStatsSystem
from Systems.TargetSystem import AddTargeterSystem, RemoveTargeterSystem, TargetSystem



class BaseLevel:
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height
        
        self.map = None

        self.e: EntityManager = EntityManager(self)
        registerComponents(self.e)
        self.systems: dict[int: list[BaseSystem]] = {}


    def registerSystem(self, actions, system):
        for action in actions:
            if action not in self.systems.keys():
                self.systems[action] = []

            self.systems[action].append(system)

    def removeSystem(self, action, system):
        self.systems[action].pop(system)


    def post(self, action, data):
        print (f"Action posted: {action}\nData: {data}")
        if action in self.systems.keys():
            for system in self.systems[action]:
                system.post(data)
        else:
            print (f"no takes for {action}")


    def update(self):
        pass



class TestLevel(BaseLevel):
    lastTime = time.time()*1000
    fps = 0
    lastFps = 0
    lowestFps = 60

    def __init__(self, app, width, height):
        super().__init__(app, width, height)
        
        self.map = LevelCreator.generateBasicLevel(self, self.width-24, self.height-14)

        self.renderQuery = self.e.createQuery(
            allOf=[Position, Render], 
            anyOf=[IsPlayer, IsItem, IsNPC],
            storeQuery='Render')

        self.lightsQuery = self.e.createQuery(
            allOf=[Position, Light],
            storeQuery='LightsOnGround'
        )

        self.itemsOnGroundQuery = self.e.createQuery(
            allOf=[IsItem, Position],
            storeQuery='ItemsOnGround'
        )

        self.playersQuery = self.e.createQuery(
            allOf=[IsPlayer],
            storeQuery = 'Players'
        )

        self.npcsQuery = self.e.createQuery(
            allOf=[IsNPC],
            storeQuery = 'NPCs'
        )

        self.actorsQuery = self.e.createQuery(
            anyOf=[IsNPC, IsPlayer],
            storeQuery = 'Actors'
        )

        self.collidableQuery = self.e.createQuery(
            allOf=[Collidable],
            storeQuery = 'Collidable'
        )

        self.initQuery = self.e.createQuery(
            allOf=[Init],
            noneOf=[IsReady],
            storeQuery = 'InitQuery'
        )

        self.moveQuery = self.e.createQuery(
            allOf=[Position],
            storeQuery = 'MoveQuery'
        )

        self.targetedQuery = self.e.createQuery(
            allOf=[Targeted],
            storeQuery = 'TargetedQuery'
        )

        self.selectionUIQuery = self.e.createQuery(
            allOf=[SelectionUI],
            storeQuery = 'SelectionUIQuery'
        )

        self.messageLogEntity = self.e.createEntity()
        self.e.addComponent(self.messageLogEntity, Position, {'x': 0, 'y': height - 14, 'width': int(width / 2), 'height': 14})
        
        self.combatLogEntity = self.e.createEntity()
        self.e.addComponent(self.combatLogEntity, Position, {'x': int(width/2), 'y': height - 14, 'width': int(width / 2), 'height': 14})

        self.messagelogSystem = MessageLogSystem(self, self.messageLogEntity)
        self.combatLogSystem = CombatLogSystem(self, self.combatLogEntity)

        self.initSystem = InitSystem(self)
        self.playerInputSystem = PlayerInputSystem(self)
        self.moveSystem = MoveSystem(self)
        self.targetSystem = TargetSystem(self)
        self.addTargeterSystem = AddTargeterSystem(self)
        self.removeTargeterSystem = RemoveTargeterSystem(self)
        self.tryPickupItemSystem = TryPickupItemSystem(self)
        self.pickupItemSystem = PickupItemSystem(self)
        self.openInventorySystem = OpenInventorySystem(self)
        self.dropItemSystem = DropItemSystem(self)
        self.updateSelectionUISystem = UpdateSelectionUISystem(self)
        self.closeUISystem = CloseUISystem(self)
        self.equipItemSystem = EquipItemSystem(self)
        self.recalculateStatsSystem = RecalculateStatsSystem(self)
        self.meleeSystem = MeleeSystem(self)
        self.damageSystem = DamageSystem(self)
        self.aiSystem = AISystem(self)
        self.deathSystem = DeathSystem(self)
        
        self.renderUISystem = RenderPlayerUISystem(self)
        self.renderEntitiesSystem = RenderEntitiesSystem(self)
        self.renderSelectionUISystem = RenderSelectionUISystem(self)



        self.e.loadEntities('objects.json')

        self.player = self.e.spawn('PLAYER', self.map.start[0], self.map.start[1])        
        self.e.addComponent(self.player, PlayerInput, {'controller': controllers[0]})

        self.e.spawn('torch', self.map.start[0], self.map.start[1]+1)
        self.e.spawn('shortsword', self.map.start[0], self.map.start[1]-1)
        self.e.spawn('torch', self.map.end[0], self.map.end[1]+1)
        # self.e.spawn('orc', self.map.start[0]-1, self.map.start[1])
        # self.e.spawn('orc', self.map.start[0]+1, self.map.start[1])

        orc = self.e.spawn('orc', self.map.end[0]-1, self.map.end[1])
        sword = self.e.spawn('shortsword', -1, -1, orc)
        
        self.post('log', {'colour': (200, 200, 200), 'message': 'Game started'})



    def update(self):
        self.initSystem.run()
        self.playerInputSystem.run()
        self.targetSystem.run()
        self.removeTargeterSystem.run()
        self.addTargeterSystem.run()
        self.tryPickupItemSystem.run()
        self.pickupItemSystem.run()
        self.updateSelectionUISystem.run()
        self.dropItemSystem.run()
        self.equipItemSystem.run()
        self.closeUISystem.run()

        self.aiSystem.run()

        self.moveSystem.run()
        self.openInventorySystem.run()
        

        self.recalculateStatsSystem.run()

        self.meleeSystem.run()
        self.damageSystem.run()

        self.map.update()

        self.map.draw(self.app.screen)
        self.messagelogSystem.run()
        self.combatLogSystem.run()
        self.renderEntitiesSystem.run()
        self.renderUISystem.run()
        self.renderSelectionUISystem.run()

        self.deathSystem.run()


        self.fps += 1
        curTime = time.time()*1000
        if curTime >= self.lastTime + 1000:
            self.lastTime = curTime
            self.lastFps = self.fps
            if self.lastFps < self.lowestFps:
                self.lowestFps = self.lastFps
            self.fps = 0
        self.app.screen.printLine(0, 0, str(self.lastFps))
        self.app.screen.printLine(0, 1, str(self.lowestFps))
        self.app.screen.printLine(0, 2, str(len(self.renderQuery.result)))        