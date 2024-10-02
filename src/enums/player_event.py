from enum import Enum
from typing import List

class PlayerEvent(Enum):
    PASSES = 'passes'
    BALL_RECEIPTS = 'ball_receipts'
    CARRYS = 'carrys'
    PRESSURES = 'pressures'
    FOUL_COMMITTEDS = 'foul_committeds'
    FOUL_WONS = 'foul_wons'
    DISPOSSESSEDS = 'dispossesseds'
    DUELS = 'duels'
    DRIBBLED_PASTS = 'dribbled_pasts'
    DRIBBLES = 'dribbles'
    CLEARANCES = 'clearances'
    BLOCKS = 'blocks'
    INTERCEPTIONS = 'interceptions'
    BALL_RECOVERYS = 'ball_recoverys'
    MISCONTROLS = 'miscontrols'
    SHIELDS = 'shields'
    SHOTS = 'shots'
    GOAL_KEEPERS = 'goal_keepers'
    INJURY_STOPPAGES = 'injury_stoppages'
    SUBSTITUTIONS = 'substitutions'
    BAD_BEHAVIOURS = 'bad_behaviours'
    FIFTY_FIFTYS = '50/50s'
    
    def to_value_list() -> List:
        return [e.value for e in PlayerEvent]