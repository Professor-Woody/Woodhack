from Levels.Creator.Generators.Caverns import createCaverns
from Levels.Creator.Generators.Caves import createCaves
from Levels.Creator.Generators.Dungeon import createDungeon
from Levels.Creator.Generators.Tunnels import *

Generators = {
    'caverns': createCaverns,
    'caves': createCaves,
    'dungeon': createDungeon,
    'tunnel': createTunnel,
    'corridor': createCorridor,
    'smallTunnel': createSmallTunnel,
    'smallCorridor': createSmallCorridor
}


