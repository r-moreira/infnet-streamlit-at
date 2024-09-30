import streamlit as st
from pandas import DataFrame
from typing import Tuple

class SelectBoxes:
    
    class State: 
        @staticmethod
        def set_competition_name(competition_name: str) -> None:
            st.session_state.competition_name = competition_name
            
        def get_competition_name() -> str:
            return st.session_state.competition_name
        
        def set_season_name(season_name: str) -> None:
            st.session_state.season_name = season_name
            
        def get_season_name() -> str:
            return st.session_state.season_name
        
        def set_team_name(team_name: str) -> None:
            st.session_state.team_name = team_name
            
        def get_team_name() -> str:
            return st.session_state.team_name
        
        def set_team_match_option(team_match_option: str) -> None:
            st.session_state.team_match_option = team_match_option
            
        def get_team_match_option() -> str:
            return st.session_state.team_match_option
    
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
            
        # SelectBoxes.State.set_competition_name(competition_name)
        # SelectBoxes.State.set_season_name(season_name)
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
        