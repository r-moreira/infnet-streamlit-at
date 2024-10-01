from abc import abstractmethod
from enum import Enum
import json
import logging
import time
from typing import List, Tuple, Dict 
import pandas as pd
from pandas import DataFrame
import plotly.express as px
from components.selectboxes import SelectBoxes
from enums.match_event import MatchEvent
from repository.statsbomb_repository import StatsBombRepository
from service.session_state_service import SessionStateService
from view.abstract_streamlit_view import AbstractStreamlitView
from view.abstract_view_strategy import AbstractViewStrategy, ViewStrategy
from enums.statsbomb_view_menu_option import StatsBombViewMenuOption
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space

# TODO: Obter dados dos eventos de partidas e jogadores do StatsBomb
# TODO: Criar visualizações com os dados de eventos obtidos
# TODO: Criar visualizações com a biblioteca MPLSoccer
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
        
        add_vertical_space(1)
        
        menu_option = self.option_menu_fragment()
        competitions = self.get_cached_competitions(self.get_competitions_list())
        competition_name, season_name, competition = SelectBoxes.select_competition_and_season(competitions)
        matches = self.get_cached_matches(competition_name, season_name, competition)
        team_name = SelectBoxes.team_select(matches)
        team_matches = self.get_cached_team_matches(matches, team_name)
        
        AbstractStatsBombView.logger.info(f"Menu option selected: {menu_option}")
        
        if menu_option == StatsBombViewMenuOption.TEAM:
            self.team_fragment(team_name, competition_name, team_matches)
        elif menu_option == StatsBombViewMenuOption.MATCH:
            self.match_fragment(team_matches)
        elif menu_option == StatsBombViewMenuOption.PLAYER:
            self.player_fragment(team_name, team_matches) 

    def option_menu_fragment(self) -> StatsBombViewMenuOption:
        menu_index = 0
        if self.session_state_service.is_view_menu_option():
            menu_index = StatsBombViewMenuOption.to_value_list().index(self.session_state_service.get_view_menu_option())

        menu_option = option_menu(
            None, 
            options=StatsBombViewMenuOption.to_value_list(), 
            icons=['people', 'play-circle', "person"], 
            menu_icon="cast",            
            default_index=menu_index,
            orientation="horizontal",
            key=f"{self.get_title()}_view_menu"
        )
        
        self.session_state_service.set_view_menu_option(menu_option)
        return StatsBombViewMenuOption(menu_option)

    def team_fragment(self, team_name: str, competition_name: str, team_matches: DataFrame) -> None:
        team_info = self.statsbomb_repository.get_team_matches_info(team_name, team_matches)
                  
        self.team_plots(team_info, competition_name) 
        
        st.divider()
        
        st.markdown(f"<h3 style='text-align: center;'>Open Data</h3>", unsafe_allow_html=True)
        
        with st.expander("Dataframe", expanded=False):
            st.dataframe(team_matches)
            st.download_button("Download", team_matches.to_csv(), "team_matches.csv", "text/csv")
      
        with st.expander("Metrics Json", expanded=False):
            st.write(team_info)
            st.download_button("Download", json.dumps(team_info, ensure_ascii=False, indent=2), "team_info.json", "application/json") 

    def match_fragment(self, team_matches: DataFrame) -> None:
        team_match_option = SelectBoxes.match_select(team_matches)
        
        match_info, match = self.statsbomb_repository.get_team_match_info(team_matches, team_match_option)
        
        events_dict = self.get_cached_split_match_events(match_info["match_id"])

        events_info = self.statsbomb_repository.get_match_events_info(events_dict)
        
        self.match_plots(match_info, events_info)     
        
        st.divider()
        
        st.markdown(f"<h3 style='text-align: center;'>Open Data</h3>", unsafe_allow_html=True)
        
       
        with st.expander("Events Dataframe", expanded=True):
            selected_event = st.selectbox("Event", MatchEvent.to_value_list(), index=2)
        
            event = self.statsbomb_repository.get_match_event(
                match_info["match_id"], 
                MatchEvent(selected_event),
                events_dict
            )
        
            selected_columns = st.multiselect("Columns", event.columns, default=event.columns)
            
            st.dataframe(event[selected_columns]) 
            st.download_button("Download", event[selected_columns].to_csv(), "match_events.csv", "text/csv")
        
        with st.expander("Match Dataframe", expanded=False):
            st.dataframe(match)
            st.download_button("Download", team_matches.to_csv(), "team_matches.csv", "text/csv") 
            
        with st.expander("Match Metrics Json", expanded=False):
            st.write(match_info)
            st.download_button("Download", json.dumps(match_info, ensure_ascii=False, indent=2), "match_info.json", "application/json")
            
        with st.expander("Events Metrics Json", expanded=False):
            st.write(events_info)
            st.download_button("Download", json.dumps(events_info, ensure_ascii=False, indent=2), "events_info.json", "application/json")
        
    def player_fragment(self, team_name: str, team_matches: DataFrame) -> None:
        team_match_option = SelectBoxes.match_select(team_matches)
        
        match_info, match = self.statsbomb_repository.get_team_match_info(team_matches, team_match_option)
        
        team_lineup = self.get_cached_team_lineup(match_info["match_id"], team_name)
        
        player_name = SelectBoxes.player_select(team_lineup)
        
        st.dataframe(team_lineup)
        
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_competitions(_self, competitions_list: List[str]) -> DataFrame:
        competitions = _self.statsbomb_repository.get_competitions()
        return competitions[competitions['competition_name'].isin(competitions_list)]
        
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_team_matches(_self, matches: DataFrame, team_name: str) -> DataFrame:
        return _self.statsbomb_repository.get_team_matches(team_name, matches)

    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_matches(_self, competition_name: str, season_name: str, competition: str) -> DataFrame:
        return _self.statsbomb_repository.get_matches(competition_name, season_name, competition)
    
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_team_lineup(_self, match_id: int, team_name: str) -> DataFrame:
        return _self.statsbomb_repository.get_team_lineup(match_id, team_name)
    
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_match_event(_self, match_id: int, match_event: MatchEvent) -> DataFrame:
        return _self.statsbomb_repository.get_match_event(match_id, match_event)
    
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_split_match_events(_self, match_id: int) -> Dict[str, DataFrame]:
        return _self.statsbomb_repository.get_split_match_events(match_id)
    
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_match_events(_self, match_id: int) -> DataFrame:
        return _self.statsbomb_repository.get_match_events(match_id)
    
    
    def match_plots(self, match_info: Dict, events_info: Dict) -> None:
        add_vertical_space(2)
        
        st.markdown(f"<h3 style='text-align: center;'>{match_info['home_team']} vs {match_info['away_team']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center;'> At {match_info['stadium']} - {match_info['match_date']}</h4>", unsafe_allow_html=True)
        
        add_vertical_space(2)
        
        col1, col2, col3, col4 = st.columns(4)
                    
        with col1:
            st.metric("Home Score", match_info["home_score"])
            
        with col2:
            st.metric("Away Score", match_info["away_score"])
            
        with col3:
            st.metric("Total Goals", match_info["home_score"] +  match_info["away_score"])
        
        with col4:
            st.metric("Total Shots", events_info["total_shots"])
            
        
        col1, col2, col3, col4 = st.columns(4)
                    
        with col1:
            st.metric("Total Passes", events_info["total_passes"])
        
        with col2:
            st.metric("Total Dribbles", events_info["total_dribbles"])
            
        with col3:
            st.metric("Total Blocks", events_info["total_blocks"])
            
        with col4:
            st.metric("Total Duels", events_info["total_duels"])
            
            
    def team_plots(self, team_info: Dict, competition_name: str) -> None:
        add_vertical_space(2)
        
        st.markdown(f"<h3 style='text-align: center;'>{team_info['team_name']} at {competition_name} </h3>", unsafe_allow_html=True)
        
        add_vertical_space(2)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Matches", team_info["total_matches"])
            
        with col2:
            st.metric("Total Wins", team_info["total_wins"])
            
        with col3:
            st.metric("Total Loses", team_info["total_losses"])
            
        with col4:
            st.metric("Total Draws", team_info["total_draws"])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Goals Scored", team_info["total_goals_scored"])
            
        with col2:
            st.metric("Total Goals Conceded", team_info["total_goals_conceded"])
            
        with col3:
            st.metric("Total Home Games", team_info["total_home_games"])
            
        with col4:
            st.metric("Total Away Games", team_info["total_away_games"])
        
        
        st.divider()
        add_vertical_space(2)
        radar_data = {
            "Metric": ["Total Wins", "Total Losses", "Total Draws", "Total Goals Scored", "Total Goals Conceded"],
            "Value": [team_info["total_wins"], team_info["total_losses"], team_info["total_draws"], team_info["total_goals_scored"], team_info["total_goals_conceded"]]
        }
        radar_df = pd.DataFrame(radar_data)
        fig_radar = px.line_polar(radar_df, r="Value", theta="Metric", line_close=True)
        fig_radar.update_traces(fill='toself')
        st.markdown(f"<h5 style='text-align: center;'>Team Performance Radar Chart</h5>", unsafe_allow_html=True)
        st.plotly_chart(fig_radar)
        
        col1, col2 = st.columns(2)
        
        goals_data = {
            "Metric": ["Goals Scored", "Goals Conceded"],
            "Count": [team_info["total_goals_scored"], team_info["total_goals_conceded"]]
        }
        goals_df = pd.DataFrame(goals_data)
        fig_goals_bar = px.bar(goals_df, x="Metric", y="Count", title="Total Goals Scored vs Conceded")
        fig_goals_pie = px.pie(goals_df, names="Metric", values="Count", title="Goals Distribution")
        
        col1.plotly_chart(fig_goals_bar)
        col2.plotly_chart(fig_goals_pie)
        
        results_data = {
            "Result": ["Wins", "Losses", "Draws"],
            "Count": [team_info["total_wins"], team_info["total_losses"], team_info["total_draws"]]
        }
        results_df = pd.DataFrame(results_data)
        fig_results_bar = px.bar(results_df, x="Result", y="Count", title="Match Results")
        fig_results_pie = px.pie(results_df, names="Result", values="Count", title="Results Distribution")
        
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_results_bar)
        col2.plotly_chart(fig_results_pie)
        
        home_away_data = {
            "Location": ["Home Games", "Away Games"],
            "Count": [team_info["total_home_games"], team_info["total_away_games"]]
        }
        home_away_df = pd.DataFrame(home_away_data)
        fig_home_away_bar = px.bar(home_away_df, x="Location", y="Count", title="Home vs Away Games")
        fig_home_away_pie = px.pie(home_away_df, names="Location", values="Count", title="Home vs Away Distribution")
        
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_home_away_bar)
        col2.plotly_chart(fig_home_away_pie)
        
        avg_goals_data = {
            "Metric": ["Average Goals Scored", "Average Goals Conceded"],
            "Count": [team_info["average_goals_scored"], team_info["average_goals_conceded"]]
        }
        avg_goals_df = pd.DataFrame(avg_goals_data)
        fig_avg_goals_bar = px.bar(avg_goals_df, x="Metric", y="Count", title="Average Goals Scored vs Conceded")
        fig_avg_goals_pie = px.pie(avg_goals_df, names="Metric", values="Count", title="Average Goals Distribution")
        
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_avg_goals_bar)
        col2.plotly_chart(fig_avg_goals_pie)