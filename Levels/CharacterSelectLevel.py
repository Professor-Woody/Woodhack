from Components import AttachedInfoPanel, CharacterSelectPane, EntityInfo, InfoPanel, IsActive, IsPlayer, IsReady, Parent, Player0, Player1, Player2, Player3, Position, Render, Selected, StatPoints, Target, ToggleUI, Stat, registerCharacterSelectComponents
from Levels.BaseLevel import BaseLevel
from Controllers import controllers
from Systems.CharacterSelect.CheckControllersSystem import CheckControllersSystem
from Systems.CharacterSelect.InfoPanelSystems import CloseInfoPanelsSystem, RenderInfoPanelsSystem
from Systems.CharacterSelect.RenderCharacterPanesSystem import RenderCharacterPanesSystem
from Systems.CharacterSelect.RenderStatDisplaySystem import RenderStatDisplaySystem
from Systems.CharacterSelect.RenderTogglesSystem import RenderTogglesSystem
from Systems.CharacterSelect.ToggleSystems import ToggleColourSystem, UpdateTogglesSystem
from Systems.CharacterSelect.UpdateCharacterPanesSystem import PanesInputSystem, UpdateCharacterPanesSystem
import Colours as colour
from Systems.CharacterSelect.UpdateNewGameSystem import UpdateNewGameSystem
from Systems.CharacterSelect.UpdateStatDisplaySystem import UpdateStatDisplaySystem


class CharacterSelectLevel(BaseLevel):
    def __init__(self, app, width, height):
        super().__init__(app, width, height)

        # have 4 character panes
        # when a use button is pressed the controller is assigned to the playerId
        # in each character pane, have the following choices:
        #   name (cycle previous names, but could also break out into a character entry window)
        #   colour (cycle)
        #   class (cycle)
        #   background (cycle)
        #   stats (4 incrementers)

        # game stats (all start at -1):
        #   strength:       increases damage        (and maybe max carry)
        #   dexterity:      increases attack        (and maybe defence)
        #   intelligence:   increases magic points  (and maybe some resistances)
        #   constitution:   increases hitpoints     (and maybe some resistances)

        # class:
        #   increases 2 of your stats by 1?

        # background:
        #   increases 2 of your stats by 1?

        # You get 3 stat points to spend
        
        registerCharacterSelectComponents(self.e)
        self.controllers = controllers.copy()
        self.players = []
        self.queries = {}


        self.unclaimedPanesQuery = self.e.createQuery(
            allOf=[CharacterSelectPane],
            noneOf=[IsActive],
            storeQuery='unclaimedPanes'
        )

        self.claimedPanesQuery = self.e.createQuery(
            allOf=[CharacterSelectPane, IsActive],
            noneOf=[IsReady],
            storeQuery='claimedPanes'
        )

        self.togglesQuery = self.e.createQuery(
            allOf=[ToggleUI, IsActive],
            storeQuery='toggles'
        )

        self.statDisplayQuery = self.e.createQuery(
            allOf=[Stat, IsActive],
            storeQuery='statDisplays'
        )

        self.childEntitiesQuery = self.e.createQuery(
            allOf=[Parent],
            storeQuery='childEntities'
        )

        self.panelsQuery = self.e.createQuery(
            allOf=[InfoPanel],
            storeQuery = 'infoPanels'
        )

        self.activePanelsQuery = self.e.createQuery(
            allOf=[InfoPanel, IsActive],
            storeQuery = 'activeInfoPanels'
        )

        self.readyPlayersQuery = self.e.createQuery(
            allOf=[CharacterSelectPane, IsReady],
            storeQuery='readyPlayers'
        )

        slots = [
            [4, 4, Player0],
            [self.width - 70, 4, Player1],
            [4, self.height - 30, Player2],
            [self.width - 70, self.height - 30, Player3]

        ]
        # yMod = -1
        for i in range(len(self.controllers)):
            # x = spacing + int(spacing/2) + (i*spacing) - 8
            # y = int(height/2) + (20 * yMod) - 8
            x = slots[i][0]
            y = slots[i][1]
            # yMod *= -1

            # character pane
            entity = self.e.createEntity()
            self.e.addComponent(entity, CharacterSelectPane)
            self.e.addComponent(entity, IsPlayer, {'id': i})
            self.e.addComponent(entity, Position, {'x': x, 'y': y, 'width': 16, 'height': 20})
            self.e.addComponent(entity, Render)
            self.e.addComponent(entity, StatPoints, {'value': 4})
            self.players.insert(0, entity)

            # this pane's tools query
            self.queries[entity] = self.e.createQuery(
                allOf=[slots[i][2]],
                storeQuery=entity
            )
            # name option

            # colour toggle
            ui = self.e.createEntity()
            self.e.addComponent(ui, ToggleUI, {
                'labels': list(colour.COLOURS.keys()), 
                'selection': list(colour.COLOURS.values()),
                'action': 'toggle_colour',
                'displaySelection': False})
            self.e.addComponent(ui, Position, {'x': x+2,'y': y+2})
            self.e.addComponent(ui, Render, {'name': 'Colour: <>'})
            self.e.addComponent(ui, slots[i][2])
            self.e.addComponent(ui, Parent, {'entity': entity})
            self.e.addComponent(ui, Selected)


            # class toggle
            ui = self.e.createEntity()
            self.e.addComponent(ui, ToggleUI, {
                'labels': ['Fighter', 'Rogue', 'Wizard'],
                'selection': ['Fighter', 'Rogue', 'Wizard'],
                'action': 'toggle_class'})
            self.e.addComponent(ui, Position, {'x': x+2,'y': y+3})
            self.e.addComponent(ui, Render, {'name': 'Class: <>'})
            self.e.addComponent(ui, slots[i][2])
            self.e.addComponent(ui, Parent, {'entity': entity})

            # background toggle

            # strength numbertoggle
            ui = self.e.createEntity()
            self.e.addComponent(ui, ToggleUI, {
                'selection': ['str'],
                'action': 'toggle_stat',
                'displaySelection': False
            })
            self.e.addComponent(ui, Render, {'name': 'Str: <>'})
            self.e.addComponent(ui, Position, {'x': x+2, 'y': y+7})
            self.e.addComponent(ui, slots[i][2])
            self.e.addComponent(ui, Parent, {'entity': entity})
            self.e.addComponent(ui, EntityInfo, {
                'image': 'O={=====>\n\n ',
                'primaryText': "** Strength **\n-------------",
                'secondaryText': "Strength is a measure of a\ncharacter's brute force.  Strength\napplies directly to damage"
            })

            ui = self.e.createEntity()
            self.e.addComponent(ui, Stat, {'name': 'str'})
            self.e.addComponent(ui, Position, {'x': x+10, 'y': y+7})
            self.e.addComponent(ui, Parent, {'entity': entity})
            



            # dex numbertoggle
            ui = self.e.createEntity()
            self.e.addComponent(ui, ToggleUI, {
                'selection': ['dex'],
                'action': 'toggle_stat',
                'displaySelection': False
            })
            self.e.addComponent(ui, Render, {'name': 'Dex: <>'})
            self.e.addComponent(ui, Position, {'x': x+2, 'y': y+8})
            self.e.addComponent(ui, slots[i][2])
            self.e.addComponent(ui, Parent, {'entity': entity})
            self.e.addComponent(ui, EntityInfo, {
                'image': '-(==>\n\n     <==)-',
                'primaryText': "** Dexterity **\n-------------",
                'secondaryText': "Dexterity is the flexibility,\naccuracy and reflexes of your\ncharacter. Dexterity is used\nwhen calculating your attack"
            })


            ui = self.e.createEntity()
            self.e.addComponent(ui, Stat, {'name': 'dex'})
            self.e.addComponent(ui, Position, {'x': x+10, 'y': y+8})
            self.e.addComponent(ui, Parent, {'entity': entity})


            # int numbertoggle
            ui = self.e.createEntity()
            self.e.addComponent(ui, ToggleUI, {
                'selection': ['int'],
                'action': 'toggle_stat',
                'displaySelection': False
            })
            self.e.addComponent(ui, Render, {'name': 'Int: <>'})
            self.e.addComponent(ui, Position, {'x': x+2, 'y': y+9})
            self.e.addComponent(ui, slots[i][2])
            self.e.addComponent(ui, Parent, {'entity': entity})

            ui = self.e.createEntity()
            self.e.addComponent(ui, Stat, {'name': 'int'})
            self.e.addComponent(ui, Position, {'x': x+10, 'y': y+9})
            self.e.addComponent(ui, Parent, {'entity': entity})


            # con numbertoggle
            ui = self.e.createEntity()
            self.e.addComponent(ui, ToggleUI, {
                'selection': ['con'],
                'action': 'toggle_stat',
                'displaySelection': False
            })
            self.e.addComponent(ui, Render, {'name': 'Con: <>'})
            self.e.addComponent(ui, Position, {'x': x+2, 'y': y+10})
            self.e.addComponent(ui, slots[i][2])
            self.e.addComponent(ui, Parent, {'entity': entity})

            ui = self.e.createEntity()
            self.e.addComponent(ui, Stat, {'name': 'con'})
            self.e.addComponent(ui, Position, {'x': x+10, 'y': y+10})
            self.e.addComponent(ui, Parent, {'entity': entity})


            # infopanel
            ui = self.e.createEntity()
            self.e.addComponent(ui, InfoPanel)
            self.e.addComponent(ui, Position, {'x': x+20, 'y': y, 'width': 40, 'height': 30})
            self.e.addComponent(ui, Render, {'name': f"Player {i}"})
            self.e.addComponent(entity, AttachedInfoPanel, {'entity': ui})
            self.e.addComponent(ui, IsActive)
            self.e.addComponent(ui, Parent, {'entity': entity})
            self.e.addComponent(ui, Target)










        self.checkControllersSystem = CheckControllersSystem(self)
        self.panesInputSystem = PanesInputSystem(self)
        self.closeInfoPanelsSystem = CloseInfoPanelsSystem(self)
        
        self.updateCharacterPanesSystem = UpdateCharacterPanesSystem(self)
        self.updateTogglesSystem = UpdateTogglesSystem(self)
        self.updateStatDisplaySystem = UpdateStatDisplaySystem(self)
        
        self.toggleColourSystem = ToggleColourSystem(self)

        self.renderCharacterPanesSystem = RenderCharacterPanesSystem(self)
        self.renderTogglesSystem = RenderTogglesSystem(self)
        self.renderStatDisplaySystem = RenderStatDisplaySystem(self)
        self.renderInfoPanelsSystem = RenderInfoPanelsSystem(self)

        self.updateNewGameSystem = UpdateNewGameSystem(self)

    def update(self):
        self.checkControllersSystem.run()
        self.panesInputSystem.run()
        self.closeInfoPanelsSystem.run()

        self.updateCharacterPanesSystem.run()
        self.updateTogglesSystem.run()
        self.updateStatDisplaySystem.run()

        self.toggleColourSystem.run()
        
        self.renderCharacterPanesSystem.run()
        self.renderTogglesSystem.run()
        self.renderStatDisplaySystem.run()
        self.renderInfoPanelsSystem.run()
        
        self.updateNewGameSystem.run()
