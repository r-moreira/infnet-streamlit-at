from typing import Dict, Literal, Tuple
from pandas import DataFrame
import pandas as pd
from statsbombpy import sb

from enums.match_event import MatchEvent

class StatsBombRepository:
    def __init__(self):
        pass

    def get_competitions(self) -> DataFrame:
        return sb.competitions()
    
    def get_matches(
            self,
            competition_name: str,
            season_name: str,
            competition: DataFrame | None = None
        ) -> DataFrame:
        
        if competition is None:
            competition = self.get_competition(competition_name)
        
        season_competitions = competition[competition["season_name"] == season_name]
        
        return sb.matches(
            season_competitions["competition_id"].values[0],
            season_competitions["season_id"].values[0]
        )
    
    def get_team_lineup(
            self,
            match_id: int,
            team_name: str
        ) -> DataFrame:
        
        return sb.lineups(match_id)[team_name]
    
    def get_match_events(
            self,
            match_id: int
        ) -> DataFrame:
        
        return sb.events(match_id)
    
    def get_split_match_events(
            self,
            match_id: int
        ) -> Dict[str, DataFrame]:
        
        return sb.events(match_id=match_id, split=True, flatten_attrs=True)   
    
    def get_team_match_info(
            self,
            team_matches: DataFrame,
            match_option: str
        ) -> Tuple[Dict, DataFrame]:
        
        match_id = team_matches[team_matches["match_option"] == match_option]["match_id"].values[0]
        
        match = team_matches[team_matches["match_id"] == match_id]
        
        return {
            "match_id": int(match_id),
            "match_date": match["match_date"].values[0],
            "home_team": match["home_team"].values[0],
            "away_team": match["away_team"].values[0],
            "home_score": int(match["home_score"].values[0]),
            "away_score": int(match["away_score"].values[0]),
            "competition_stage": match["competition_stage"].values[0],
            "stadium": match["stadium"].values[0],
        }, match
        
    def get_team_matches_info(
            self,
            team_name: str,
            team_matches: DataFrame
        ) -> Dict:
        
        total_wins = 0
        total_losses = 0
        total_draws = 0
        total_goals_scored = 0
        total_goals_conceded = 0
        total_home_games = 0
        total_away_games = 0
        
        for _, match in team_matches.iterrows():
            if match['home_team'] == team_name:
                total_home_games += 1
                total_goals_scored += match['home_score']
                total_goals_conceded += match['away_score']
                if match['home_score'] > match['away_score']:
                    total_wins += 1
                elif match['home_score'] < match['away_score']:
                    total_losses += 1
                else:
                    total_draws += 1
            elif match['away_team'] == team_name:
                total_away_games += 1
                total_goals_scored += match['away_score']
                total_goals_conceded += match['home_score']
                if match['away_score'] > match['home_score']:
                    total_wins += 1
                elif match['away_score'] < match['home_score']:
                    total_losses += 1
                else:
                    total_draws += 1
                
        total_matches = len(team_matches)
        average_goals_scored = total_goals_scored / total_matches if total_matches > 0 else 0
        average_goals_conceded = total_goals_conceded / total_matches if total_matches > 0 else 0
        
        return {
            "stadium": team_matches["stadium"].values[0],
            "team_name": team_name,
            "total_matches": total_matches,
            "total_wins": total_wins,
            "total_losses": total_losses,
            "total_draws": total_draws,
            "total_goals_scored": total_goals_scored,
            "total_goals_conceded": total_goals_conceded,
            "average_goals_scored": average_goals_scored,
            "average_goals_conceded": average_goals_conceded,
            "total_home_games": total_home_games,
            "total_away_games": total_away_games
        }
    
    def get_match_events_info(self, split_events_dict: Dict[str, DataFrame]) -> Dict:
        return {
            "total_passes": len(split_events_dict[MatchEvent.PASSES.value]),
            "total_shots": len(split_events_dict[MatchEvent.SHOTS.value]),
            "total_dribbles": len(split_events_dict[MatchEvent.DRIBBLES.value]),
            "total_blocks": len(split_events_dict[MatchEvent.BLOCKS.value]),
            "total_duels": len(split_events_dict[MatchEvent.DUELS.value]),
        }
        
    def get_player_events_info(self, player_name: str, split_events_dict: Dict[str, pd.DataFrame]) -> Dict:
        player_events = {
            MatchEvent.PASSES.value: 0,
            MatchEvent.SHOTS.value: 0,
            MatchEvent.DRIBBLES.value: 0,
            MatchEvent.BLOCKS.value: 0,
            MatchEvent.DUELS.value: 0,
        }
        
        for event_name, event_df in split_events_dict.items():
            if "player" not in event_df.columns:
                continue
            player_event_df = event_df[event_df["player"] == player_name]
            player_events[event_name] = len(player_event_df)
        
        return {
            "total_passes": player_events[MatchEvent.PASSES.value],
            "total_shots": player_events[MatchEvent.SHOTS.value],
            "total_dribbles": player_events[MatchEvent.DRIBBLES.value],
            "total_blocks": player_events[MatchEvent.BLOCKS.value],
            "total_duels": player_events[MatchEvent.DUELS.value],
        }