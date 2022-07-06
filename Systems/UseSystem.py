from Actions.UseActions import MeleeAction
from Systems.BaseSystem import BaseSystem

class UseSystem(BaseSystem):
    def __init__(self, systemsManager):
        super().__init__(systemsManager, 'UseSubSystems')
        
