from typing import Dict
from pandas import DataFrame
from statsbombpy import sb

class StatsBombRepository:
    def __init__(self):
        pass

    def get_competitions(self) -> DataFrame:
        return sb.competitions()
    
    def get_competition(self, competition_name: str) -> DataFrame:
        competitions = self.get_competitions()
        
        return competitions[competitions["competition_name"] == competition_name]
    
    def get_matches(self, competition_name: str, season_name: str) -> DataFrame:
        competition = self.get_competition(competition_name)
        
        season_competitions = competition[competition["season_name"] == season_name]
        
        return sb.matches(
            season_competitions["competition_id"].values[0],
            season_competitions["season_id"].values[0]
        )
    
    def get_team_matches(self, competition_name: str, season_name: str, team_name: str) -> DataFrame:
        matches = self.get_matches(competition_name, season_name)
        
        team_matches = matches[
            (matches["home_team"] == team_name) | (matches["away_team"] == team_name)
        ]
        
        
        team_matches["match_option"] = team_matches.apply(
            lambda row: f"{row['match_date']}: {row['home_team']} vs {row['away_team']}",
            axis=1
        )
        
        return team_matches
    
    def get_team_match(self, team_matches: DataFrame, match_option: str) -> Dict:
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
        }
        