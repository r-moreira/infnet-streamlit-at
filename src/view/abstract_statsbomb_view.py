from abc import abstractmethod
from enum import Enum
import logging
import time
from typing import List, Tuple 
from pandas import DataFrame
from components.selectboxes import SelectBoxes
from repository.statsbomb_repository import StatsBombRepository
from service.session_state_service import SessionStateService
from view.abstract_streamlit_view import AbstractStreamlitView
from view.abstract_view_strategy import AbstractViewStrategy, ViewStrategy
from enums.statsbomb_view_menu_option import StatsBombViewMenuOption
import streamlit as st
from streamlit_option_menu import option_menu


class AbstractStatsBombView(AbstractStreamlitView, AbstractViewStrategy):
    logger = logging.getLogger(__name__)

    def __init__(
            self,
            statsbomb_repository: StatsBombRepository,
            session_state_service: SessionStateService
        ) -> None:
        self.statsbomb_repository = statsbomb_repository
        self.session_state_service = session_state_service

    @abstractmethod
    def get_competitions_list(self) -> List[str]:
        pass
    
    @abstractmethod
    def accept(self, view_strategy: ViewStrategy) -> bool:
        pass
    
    @abstractmethod
    def get_title(self) -> str:
        pass
    
    def render(self) -> None:
        st.title(self.get_title())
        
        menu_option = self.option_menu_fragment()
        competitions = self.get_cached_competitions(self.get_competitions_list())
        competition_name, season_name, competition = SelectBoxes.select_competition_and_season(competitions)
        matches = self.get_cached_matches(competition_name, season_name, competition)
        team_name = SelectBoxes.team_select(matches)
        team_matches = self.get_cached_team_matches(competition_name, season_name, matches, team_name)
        
        AbstractStatsBombView.logger.info(f"Menu option selected: {menu_option}")
      
        
        if menu_option == StatsBombViewMenuOption.TEAM.value:
            self.team_fragment()
        elif menu_option == StatsBombViewMenuOption.MATCH.value:
            self.match_fragment(team_matches)
        elif menu_option == StatsBombViewMenuOption.PLAYER.value:
            self.player_fragment() 

    def option_menu_fragment(self):
        menu_index = 0
        if self.session_state_service.is_view_menu_option():
            menu_index = StatsBombViewMenuOption.to_list().index(self.session_state_service.get_view_menu_option())

        menu_option = option_menu(
            None, 
            options=StatsBombViewMenuOption.to_list(), 
            icons=['house', 'cloud-upload', "list-task"], 
            menu_icon="cast",            
            default_index=menu_index,
            orientation="horizontal",
            key="world_cups_view_menu"
        )
        
        self.session_state_service.set_view_menu_option(menu_option)
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
    def get_cached_competitions(_self, competitions_list: List[str]):
        competitions = _self.statsbomb_repository.get_competitions()
        return competitions[competitions['competition_name'].isin(competitions_list)]
        
    @st.cache_data(ttl=3600)
    def get_cached_team_matches(_self, competition_name, season_name, matches, team_name):
        return _self.statsbomb_repository.get_team_matches(competition_name, season_name, team_name, matches)

    @st.cache_data(ttl=3600)
    def get_cached_matches(_self, competition_name, season_name, competition):
        return _self.statsbomb_repository.get_matches(competition_name, season_name, competition)           
            