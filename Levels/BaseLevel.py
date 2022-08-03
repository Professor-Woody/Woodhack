from EntityManager import EntityManager, Position, Render
from Levels.LevelCreator import LevelCreator, NewLevelCreator
from Components import *
from Systems.ActorSystems.AISystem import AISystem
from Systems.BaseSystem import BaseSystem
from Systems.ActorSystems.InitSystem import InitSystem
from Systems.UseSystems.HealingSystem import HealingSystem
from Systems.UseSystems.MeleeSystem import DamageSystem, DeathSystem, MeleeSystem
from Systems.Items.ProjectileSystem import UpdateProjectilesSystem
from Systems.UseSystems.RangedSystem import RangedSystem
from Systems.LevelSystems.MapSystems import RenderMapSystem, UpdateMapSystem
from Systems.LevelSystems.MessageLogSystem import CombatLogSystem, MessageLogSystem
from Systems.ActorSystems.MoveSystem import MoveSystem
from Systems.ActorSystems.PlayerInputSystem import PlayerInputSystem
from Systems.RenderSystems import CloseUISystem, RenderEntitiesSystem, RenderPlayerUISystem, RenderSelectionUISystem, UpdateSelectionUISystem
from Systems.ActorSystems.InventorySystem import *
import time
from Systems.ActorSystems.StatsSystem import RecalculateStatsSystem
from Systems.ActorSystems.TargetSystem import AddTargeterSystem, RemoveTargeterSystem, TargetSystem



class BaseLevel:
    needsSorting = False
    map = None
    def __init__(self, app, width, height):
        self.app = app
        self.width = width
        self.height = height

        self.e: EntityManager = EntityManager(self)
        registerComponents(self.e)
        self.actions: dict[str: list[BaseSystem]] = {}
        self.systems = {}
        self.activeSystems = []


    def registerSystem(self, priority, system, active):
        print (f"Registering {priority}: {system}, {active}")
        self.systems[priority] = system
        if active:
            self.activeSystems.append(priority)


    def registerActions(self, priority, actions):
        for action in actions:
            if action not in self.actions.keys():
                self.actions[action] = []

            self.actions[action].append(priority)

    def removeSystem(self, action, priority):
        self.actions[action].pop(priority)
        self.systems.pop(priority)

    def activateSystem(self, priority):
        if priority not in self.activeSystems:
            # print (f"activating system: {self.systems[priority]}")
            self.activeSystems.append(priority)
            self.activeSystems.sort()

    def deactivateSystem(self, priority):
        self.activeSystems.remove(priority)
        # self.activeSystems.sort()

    def runSystems(self):
        lastKey = -10000
        for key in self.activeSystems:
            if key > lastKey:
                lastKey = key
                # print (self.activeSystems)
                # print (f"running system: {self.systems[key]}")
                self.systems[key].run()


    def post(self, action, data):
        print (f"Action posted: {action}\nData: {data}")
        if action in self.actions.keys():
            systems = self.actions[action]
            for system in systems:
                self.systems[system].post(data)
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
        
        #self.map = LevelCreator.generateBasicLevel(self, self.width-24, self.height-14)
        self.map = NewLevelCreator.generateLevel(self, width-24, self.height-16, 'caverns')
        # =====================
        # queries
        self.projectilesQuery = self.e.createQuery(allOf=[Projectile],storeQuery='Projectiles')
        self.renderQuery = self.e.createQuery(allOf=[Position, Render], anyOf=[IsPlayer, IsItem, IsNPC],storeQuery='Render')
        self.lightsQuery = self.e.createQuery(allOf=[Position, Light],storeQuery='LightsOnGround') 
        self.itemsOnGroundQuery = self.e.createQuery(allOf=[IsItem, Position],storeQuery='ItemsOnGround')
        self.playersQuery = self.e.createQuery(allOf=[IsPlayer],storeQuery = 'Players')
        self.npcsQuery = self.e.createQuery(allOf=[IsNPC],storeQuery = 'NPCs')
        self.actorsQuery = self.e.createQuery(anyOf=[IsNPC, IsPlayer],storeQuery = 'Actors')
        self.collidableQuery = self.e.createQuery(allOf=[Collidable],storeQuery = 'Collidable')
        self.initQuery = self.e.createQuery(allOf=[Init],noneOf=[IsReady],storeQuery = 'InitQuery')
        self.moveQuery = self.e.createQuery(allOf=[Position],storeQuery = 'MoveQuery')
        self.targetedQuery = self.e.createQuery(allOf=[Targeted],storeQuery = 'TargetedQuery')
        self.selectionUIQuery = self.e.createQuery(allOf=[SelectionUI],storeQuery = 'SelectionUIQuery')

        # =====================
        # logs
        self.messageLogEntity = self.e.createEntity()
        self.e.addComponent(self.messageLogEntity, Position, {'x': 0, 'y': height - 14, 'width': int(width / 2), 'height': 14})
        self.combatLogEntity = self.e.createEntity()
        self.e.addComponent(self.combatLogEntity, Position, {'x': int(width/2), 'y': height - 14, 'width': int(width / 2), 'height': 14})
        self.messagelogSystem = MessageLogSystem(self, self.messageLogEntity)
        self.combatLogSystem = CombatLogSystem(self, self.combatLogEntity)


        # =====================
        # systems
        InitSystem(self)
        PlayerInputSystem(self)
        MoveSystem(self)
        TargetSystem(self)
        AddTargeterSystem(self)
        RemoveTargeterSystem(self)
        TryPickupItemSystem(self)
        PickupItemSystem(self)
        OpenInventorySystem(self)
        DropItemSystem(self)
        UpdateSelectionUISystem(self)
        CloseUISystem(self)
        EquipItemSystem(self)
        RecalculateStatsSystem(self)
        MeleeSystem(self)
        RangedSystem(self)
        UpdateProjectilesSystem(self)
        DamageSystem(self)
        AISystem(self)
        DeathSystem(self)
        
        UpdateMapSystem(self)
        RenderMapSystem(self)
        RenderPlayerUISystem(self)
        RenderEntitiesSystem(self)
        RenderSelectionUISystem(self)
        HealingSystem(self)

        # =====================
        # loading entity defs
        self.e.loadEntities('objects.json')

        self.e.spawn('torch', self.map.startSpot[0], self.map.startSpot[1]+1)
        self.e.spawn('shortsword', self.map.startSpot[0], self.map.startSpot[1]-1)
        self.e.spawn('torch', self.map.endSpot[0], self.map.endSpot[1]+1)
        # self.e.spawn('orc', self.map.start[0]-1, self.map.start[1])
        # self.e.spawn('orc', self.map.start[0]+1, self.map.start[1])

        # orc = self.e.spawn('orc', self.map.end[0]-1, self.map.end[1])
        # sword = self.e.spawn('shortsword', -1, -1, orc)
        
        self.post('log', {'colour': (200, 200, 200), 'message': 'Game started'})



    def update(self):
        self.runSystems()

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