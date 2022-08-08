import Helpers.PositionHelper as PositionHelper
from random import randint, choice
import numpy as np
from random import randint, choice
from EntityManager import add_bit
from Levels.Creator.Tiles import *

# TILES
floor = newTile(
    passable=True, 
    transparent=True,
    dark=(ord(" "), (100,100,100), (10, 10, 10)),
    light=(ord(" "), (200, 200, 200), (100, 100, 100)),
)

ground = newTile(
    passable=True, 
    transparent=True,
    dark=(ord("."), (100,100,100), (10, 10, 10)),
    light=(ord("."), (200, 200, 200), (100, 100, 100)),
)

wall = newTile(
    passable=False, 
    transparent=False, 
    dark=(ord("#"), (100,100,100), (10, 10, 10)),
    light=(ord("#"), (200, 200, 200), (100, 100, 100)),
)

wall2 = newTile(
    passable=False, 
    transparent=False, 
    dark=(ord("█"), (100,100,100), (10, 10, 10)),
    light=(ord("█"), (200, 200, 200), (100, 100, 100)),
)





generators = {
    "caverns": createCaverns,
    "dungeon": createDungeon,
    "caves": createCaves,
    "tunnel": createTunnel,
    "corridor": createCorridor,
    "smallTunnel": createSmallTunnel,
    "smallCorridor": createSmallCorridor
}
