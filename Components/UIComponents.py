from dataclasses import dataclass
from Components.Components import Initiative, Position, Render, Stats
from Components.FlagComponents import IsEquipped, IsReady
from Components.InventoryComponents import Body
from ecstremity import Component
from Components.PlayerInputComponents import PlayerInput
import Colours as colour
from ecstremity.entity import Entity


class SelectionUI(Component):
    def __init__(self, parentEntity, selectionList, commands):
        self.selectionIndex = 0
        self.parentEntity = parentEntity
        self.selectionList = selectionList
        # format for commands:
        # ['eventname', {'data': ....}]
        self.commands = commands
        print ("UI Opened")



    def on_update(self, action):
        # if not self.parentEntity[PlayerInput].controlFocus:
        #     self.entity.destroy()
        if self.entity != self.parentEntity[PlayerInput].controlFocus[-1]:
            return
        dy = 0
        if self.parentEntity[PlayerInput].controller.getPressedOnce('up'):
            dy -= 1
        elif self.parentEntity[PlayerInput].controller.getPressedOnce('down'):
            dy += 1

        self.selectionIndex += dy
        if self.selectionIndex < 0:
            self.selectionIndex = len(self.selectionList)-1
        elif self.selectionIndex >= len(self.selectionList):
            self.selectionIndex = 0        

        for command in self.commands.keys():
            if self.parentEntity[PlayerInput].controller.getPressedOnce(command):
                self.commands[command]["target"].fire_event(
                    self.commands[command]["command"], 
                    self.commands[command]["data"])

    def on_close_UI(self, action):
        print ("UI Closed")
        self.parentEntity[PlayerInput].controlFocus.remove(self.entity)
        self.entity.destroy()

    def on_render(self, action):
        screen = action.data.level.app.screen
        position = self.entity[Position]
        fg = self.parentEntity[Render].fg

        screen.drawFrame(
            position.x,
            position.y,
            position.width,
            position.height,
            title=f"{self.parentEntity[Render].entityName}'s Inventory",
            bg=colour.BLACK,
            fg=fg
            )
        
        for i in range(len(self.selectionList)):
            bg = colour.BLACK
            if i == self.selectionIndex:
                bg = colour.GREY
            
            name = self.selectionList[i][Render].entityName
            if self.selectionList[i].has(IsEquipped):
                name += f"-{self.selectionList[i][IsEquipped].slot}"
            
            screen.printLine(
                position.x+1,
                position.y+1+i,
                name,
                bg=bg
            )

@dataclass
class CharacterInfoUI(Component):
    parentEntity: Entity

    def on_render(self, action):
        screen = action.data.level.app.screen
        # draw a box down below with the following:
        # HP
        # speed left
        # left hand
        # right hand
        stats = self.parentEntity[Stats]
        body = self.parentEntity[Body]
        speed = self.parentEntity[Initiative].speed
        fg = self.parentEntity[Render].fg
        position = self.entity[Position]

        screen.drawFrame(
            position.x,
            position.y,
            position.width,
            position.height,
            title=f"{self.parentEntity[Render].entityName}",
            bg=colour.BLACK,
            fg=fg
            )

        screen.printLine(
            position.x+1,
            position.y+1,
            f"HP: {stats.hp} / {stats.maxHp}"
        )
        if speed:
            screen.printLine(
                position.x+1,
                position.y+2,
                f"Cooldown: {speed}",
                bg=colour.RED
            )
        else:
            screen.printLine(
                position.x+1,
                position.y+2,
                f"Ready",
                bg=colour.GREEN
            )
        lefthand = 'Empty'
        lbg = colour.BLACK
        if body.slots['lefthand']:
            lefthand = body.slots['lefthand'][Render].entityName
            if body.slots['lefthand'].has(IsReady):
                lbg = colour.GREEN
            else:
                lbg = colour.RED

        righthand = 'Empty'
        rbg = colour.BLACK
        if body.slots['righthand']:
            righthand = body.slots['righthand'][Render].entityName
            if body.slots['righthand'].has(IsReady):
                rbg = colour.GREEN
            else:
                rbg = colour.RED



        screen.printLine(
            position.x+1,
            position.y+3,
            f"left hand: {lefthand}",
            bg=lbg
        )

        screen.printLine(
            position.x+1,
            position.y+3,
            f"right hand: {righthand}",
            bg=rbg
        )