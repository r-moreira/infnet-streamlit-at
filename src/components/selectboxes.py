import streamlit as st
from pandas import DataFrame
from typing import Tuple

class SelectBoxes:
        
    @staticmethod
    def select_competition_and_season(competitions: DataFrame) -> Tuple[str, str, DataFrame]:
        col1, col2 = st.columns(2)
        
        with col1:
            competition_name = st.selectbox(
                "Competition",
                competitions["competition_name"].unique()
            )
        
        with col2:
            competition = competitions[competitions["competition_name"] == competition_name]
    
            
            season_name = st.selectbox(
                "Season",
                competition["season_name"].unique()
            )
            
        return competition_name, season_name, competition
    
    @staticmethod
    def team_select(matches: DataFrame) -> str:
        team_name = st.selectbox(
            "Team Name",
            matches["home_team"].unique()
        )
        
        return team_name
    
    @staticmethod
    def match_select(team_matches: DataFrame) -> str:
        team_match_option = st.selectbox(
            "Match",
            team_matches["match_option"].unique()
        )
        
        return team_match_option
    
    @staticmethod
    def player_select(team_lineup: DataFrame) -> str:
        player_name = st.selectbox(
            "Player",
            team_lineup["player_name"].unique()
        )
        
        return player_name