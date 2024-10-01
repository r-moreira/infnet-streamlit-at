    
from enum import Enum
from typing import List

class StatsBombViewMenuOption(Enum):
    TEAM = "Team"
    MATCH = "Match"
    PLAYER = "Player"

    def to_list() -> List:
        return [e.value for e in StatsBombViewMenuOption]