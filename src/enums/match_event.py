from enum import Enum
from typing import List


class MatchEvent(Enum):
    STARTING_XIS = 'starting_xis'
    HALF_STARTS = 'half_starts'
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
    REFEREE_BALL_DROPS = 'referee_ball_drops'
    HALF_ENDS = 'half_ends'
    SUBSTITUTIONS = 'substitutions'
    BAD_BEHAVIOURS = 'bad_behaviours'
    TACTICAL_SHIFTS = 'tactical_shifts'
    FIFTY_FIFTYS = '50/50s'
    
    
    def to_value_list() -> List:
        return [e.value for e in MatchEvent]