from enum import Enum
import logging
import time
from typing import List, Tuple 
from pandas import DataFrame
from components.selectboxes import SelectBoxes
from repository.statsbomb_repository import StatsBombRepository
from service.session_state_service import SessionStateService
from view.abstract_view_strategy import AbstractViewStrategy, ViewStrategy
import streamlit as st
from streamlit_option_menu import option_menu



#How to preserve session state in Streamlit: https://discuss.streamlit.io/t/multi-page-apps-with-widget-state-preservation-the-simple-way/22303/8
class WorldCupsView(AbstractViewStrategy):
    logger = logging.getLogger(__name__)
    
    class MenuOption(Enum):
        TEAM = "Team"
        MATCH = "Match"
        PLAYER = "Player"
    
        def to_list() -> List:
           return [e.value for e in WorldCupsView.MenuOption]
    
    class State:
        @staticmethod
        def set_view_menu_option(menu_option: str) -> None:
            if menu_option not in WorldCupsView.MenuOption.to_list():
                raise ValueError(f"Invalid menu option: {menu_option}")

            st.session_state['world_cups_view_menu_option'] = menu_option
            
        @staticmethod
        def get_view_menu_option() -> str:
            if 'world_cups_view_menu_option' not in st.session_state:
                WorldCupsView.State.set_view_menu_option(WorldCupsView.MenuOption.TEAM.value)
            
            return st.session_state['world_cups_view_menu_option']
    
    def __init__(
            self,
            statsbomb_repository: StatsBombRepository,
            session_state_service: SessionStateService
        ) -> None:
        self.statsbomb_repository = statsbomb_repository
        self.session_state_service = session_state_service
    
    def accept(self, view_strategy: ViewStrategy) -> bool:
        return view_strategy == ViewStrategy.WORLD_CUPS
    
    def render(self) -> None:
        st.title("World Cup Analysis")
        
        menu_option = self.option_menu_fragment()
        competitions = self.get_cached_competitions()
        competition_name, season_name, competition = SelectBoxes.select_competition_and_season(competitions)
        matches = self.get_cached_matches(competition_name, season_name, competition)
        team_name = SelectBoxes.team_select(matches)
        team_matches = self.get_cached_team_matches(competition_name, season_name, matches, team_name)
        
        if menu_option == self.MenuOption.TEAM:
            self.team_fragment()
        elif menu_option == self.MenuOption.MATCH:
            self.match_fragment(team_matches)
        elif menu_option == self.MenuOption.PLAYER:
            self.player_fragment() 

    def option_menu_fragment(self):
        menu_index = 0
        if 'world_cups_view_menu_option' in st.session_state:
            menu_index = self.MenuOption.to_list().index(self.State.get_view_menu_option())

        menu_option = option_menu(
            None, 
            options=self.MenuOption.to_list(), 
            icons=['house', 'cloud-upload', "list-task"], 
            menu_icon="cast",            
            default_index=menu_index,
            orientation="horizontal",
            key="world_cups_view_menu"
        )
        
        self.State.set_view_menu_option(menu_option)
        return menu_option

    def team_fragment(self) -> None:
        st.write("In Progress")

    def match_fragment(self, team_matches: DataFrame) -> None:
        team_match_option = SelectBoxes.match_select(team_matches)

        match_info = self.statsbomb_repository.get_team_match(team_matches, team_match_option)
        
        with st.expander("Match Info"):
            st.write(match_info)
        
        st.dataframe(team_matches)
        
    def player_fragment(self) -> None:
        st.write("In Progress")
        
    
    @st.cache_data(ttl=3600)
    def get_cached_competitions(_self):
        competitions = _self.statsbomb_repository.get_competitions()
        
        return competitions[competitions['competition_name'].isin([
            "FIFA U20 World Cup", 
            "FIFA World Cup", 
            "Women's World Cup"
        ])]
        
    
    @st.cache_data(ttl=3600)
    def get_cached_team_matches(_self, competition_name, season_name, matches, team_name):
        return _self.statsbomb_repository.get_team_matches(competition_name, season_name, team_name, matches)

    @st.cache_data(ttl=3600)
    def get_cached_matches(_self, competition_name, season_name, competition):
        return _self.statsbomb_repository.get_matches(competition_name, season_name, competition)           
            