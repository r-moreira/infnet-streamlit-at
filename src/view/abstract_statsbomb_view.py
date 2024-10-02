from abc import abstractmethod
from enum import Enum
import json
import logging
import time
from typing import List, Tuple, Dict 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mplsoccer import Pitch
import seaborn as sns
import pandas as pd
from pandas import DataFrame
import plotly.express as px
from components.selectboxes import SelectBoxes
from enums.match_event import MatchEvent
from enums.player_event import PlayerEvent
from repository.statsbomb_repository import StatsBombRepository
from service.session_state_service import SessionStateService
from view.abstract_streamlit_view import AbstractStreamlitView
from view.abstract_view_strategy import AbstractViewStrategy, ViewStrategy
from enums.statsbomb_view_menu_option import StatsBombViewMenuOption
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space


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
        
        with st.expander("Matches Dataframe", expanded=False):
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
        
            event = self.get_cached_match_event(match_info["match_id"], MatchEvent(selected_event))
            
            if event is not None:
                selected_columns = st.multiselect("Columns", event.columns, default=event.columns)
                
                st.dataframe(event[selected_columns]) 
                st.download_button("Download", event[selected_columns].to_csv(), "match_events.csv", "text/csv")
            else:
                add_vertical_space(1)
                st.warning(f"Event {selected_event} not found in the match")
        
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
        
        match_info, _ = self.statsbomb_repository.get_team_match_info(team_matches, team_match_option)
        
        team_lineup = self.get_cached_team_lineup(match_info["match_id"], team_name)
        
        player_name = SelectBoxes.player_select(team_lineup)
        
        match_event_dict = self.get_cached_split_match_events(match_info["match_id"])
        
        player_events_info = self.statsbomb_repository.get_player_events_info(player_name, match_event_dict)
        
        self.player_plots(player_name, player_events_info, match_info)        
        
        st.divider()
        
        st.markdown(f"<h3 style='text-align: center;'>Open Data</h3>", unsafe_allow_html=True)
        
        with st.expander("Lineup Dataframe", expanded=True):
            st.dataframe(team_lineup)
            st.download_button("Download", team_lineup.to_csv(), "team_lineup.csv", "text/csv")
        
        with st.expander("Events Dataframe", expanded=False):
            selected_event = st.selectbox("Event", PlayerEvent.to_value_list(), index=0)
            
            event = self.get_cached_player_event(match_info, player_name, selected_event)
            
            if event is not None:
                selected_columns = st.multiselect("Columns", event.columns, default=event.columns)
                    
                st.dataframe(event[selected_columns]) 
                st.download_button("Download", event[selected_columns].to_csv(), "player_events.csv", "text/csv")

            else:
                add_vertical_space(2)
                st.warning(f"Event {selected_event} not found for player {player_name}")
                
        with st.expander("Events Metrics Json", expanded=False):
            st.write(player_events_info)
            st.download_button("Download", json.dumps(player_events_info, ensure_ascii=False, indent=2), "player_events_info.json", "application/json")
        
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_competitions(_self, competitions_list: List[str]) -> DataFrame:
        competitions = _self.statsbomb_repository.get_competitions()
        return competitions[competitions['competition_name'].isin(competitions_list)]
        
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_team_matches(_self, matches: DataFrame, team_name: str) -> DataFrame:
        team_matches = matches[
            (matches["home_team"] == team_name) | (matches["away_team"] == team_name)
        ]
        
        team_matches["match_option"] = team_matches.apply(
            lambda row: f"{row['match_date']}: {row['home_team']} vs {row['away_team']}",
            axis=1
        )
        return team_matches   

    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_matches(_self, competition_name: str, season_name: str, competition: str) -> DataFrame:
        return _self.statsbomb_repository.get_matches(competition_name, season_name, competition)
    
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_team_lineup(_self, match_id: int, team_name: str) -> DataFrame:
        return _self.statsbomb_repository.get_team_lineup(match_id, team_name)

    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_split_match_events(_self, match_id: int) -> Dict[str, DataFrame]:
        return _self.statsbomb_repository.get_split_match_events(match_id)
    
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_match_event(_self, match_id: int, event: MatchEvent | PlayerEvent) -> DataFrame:
        match_events_dict = _self.get_cached_split_match_events(match_id)
        match_event = match_events_dict.get(event.value)
        
        if type(match_event) is not DataFrame:
            return None
        
        return match_event
    
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_player_event(_self, match_info: Dict, player_name: str, selected_event: str) -> DataFrame | None:
        match_event = _self.get_cached_match_event(match_info["match_id"], MatchEvent(selected_event))
        
        try:
            return match_event[match_event["player"] == player_name]
        except Exception as e:
            AbstractStatsBombView.logger.debug(f"Player {player_name} not found in the match selected event: {selected_event}")
            return None
    
    @st.cache_data(ttl=3600, show_spinner=True)
    def get_cached_team_event(_self, match_info: Dict, team_name: str, selected_event: str) -> DataFrame | None:
        match_event = _self.get_cached_match_event(match_info["match_id"], MatchEvent(selected_event))
        
        try:
            return match_event[match_event["team"] == team_name]
        except Exception as e:
            AbstractStatsBombView.logger.debug(f"Team {team_name} not found in the match selected event: {selected_event}")
            return None
            
    def team_plots(self, team_info: Dict, competition_name: str) -> None:
        add_vertical_space(2)
        
        st.markdown(f"<h3 style='text-align: center;'>{team_info['team_name']} at {competition_name} </h3>", unsafe_allow_html=True)
        
        add_vertical_space(2)
        
        _, col1, col2, col3, col4, _ = st.columns([1, 3, 3, 3, 3, 1], gap="large")
        
        with col1:
            st.metric("Matches", team_info["total_matches"])
            
        with col2:
            st.metric("Wins", team_info["total_wins"])
            
        with col3:
            st.metric("Loses", team_info["total_losses"])
            
        with col4:
            st.metric("Draws", team_info["total_draws"])
        
        _, col1, col2, col3, col4, _ = st.columns([1, 3, 3, 3, 3, 1], gap="large")
        
        with col1:
            st.metric("Goals Scored", team_info["total_goals_scored"])
            
        with col2:
            st.metric("Goals Conceded", team_info["total_goals_conceded"])
            
        with col3:
            st.metric("Home Games", team_info["total_home_games"])
            
        with col4:
            st.metric("Away Games", team_info["total_away_games"])
        
        
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
        
    def match_plots(self, match_info: Dict, events_info: Dict) -> None:
        add_vertical_space(2)
        
        st.markdown(f"<h3 style='text-align: center;'>{match_info['home_team']} vs {match_info['away_team']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center;'> At {match_info['stadium']} - {match_info['match_date']}</h4>", unsafe_allow_html=True)
        
        add_vertical_space(2)
        
        _, col1, col2, col3, col4, _ = st.columns([1, 3, 3, 3, 3, 1], gap="large")
                    
        with col1:
            st.metric(f"{match_info['home_team']} Score", match_info["home_score"])
            
        with col2:
            st.metric(f"{match_info['away_team']} Score", match_info["away_score"])
            
        with col3:
            st.metric("Total Goals", match_info["home_score"] +  match_info["away_score"])
        
        with col4:
            st.metric("Total Shots", events_info["total_shots"])
            
        
        _, col1, col2, col3, col4, _ = st.columns([1, 3, 3, 3, 3, 1], gap="large")
                    
        with col1:
            st.metric("Total Passes", events_info["total_passes"])
        
        with col2:
            st.metric("Total Dribbles", events_info["total_dribbles"])
            
        with col3:
            st.metric("Total Blocks", events_info["total_blocks"])
            
        with col4:
            st.metric("Total Duels", events_info["total_duels"])
            
        
        st.divider()
 
        st.markdown(f"<h3 style='text-align: center;'>Shots by {match_info['home_team']}</h3>", unsafe_allow_html=True)
        
        add_vertical_space(1)
        
        shot_events_home = self.get_cached_team_event(match_info, match_info["home_team"], 'shots').reset_index()
        shot_events_away = self.get_cached_team_event(match_info, match_info["away_team"], 'shots').reset_index()
        shots_coords_home = shot_events_home['location']
        shots_coords_home = pd.DataFrame(shots_coords_home.to_list(), columns=['x', 'y'])
        shots_coords_away = shot_events_away['location']
        shots_coords_away = pd.DataFrame(shots_coords_away.to_list(), columns=['x', 'y'])
        
        add_vertical_space(1)
        
        self.plot_team_shots(shot_events_home, shots_coords_home)
        
        add_vertical_space(2)
        
        st.markdown(f"<h3 style='text-align: center;'>Shots by {match_info['away_team']}</h3>", unsafe_allow_html=True)
        
        self.plot_team_shots(shot_events_away, shots_coords_away)
        
            
    def player_plots(self, player_name: str, events_info: Dict, match_info: Dict) -> None:
        add_vertical_space(2)
            
        st.markdown(f"<h3 style='text-align: center;'>{player_name}</h3>", unsafe_allow_html=True)
            
        add_vertical_space(2)
        
        _, col1, col2, col3, col4, _ = st.columns([1, 3, 3, 3, 3, 1], gap="large")
                    
        with col1:
            st.metric("Total Passes", events_info["total_passes"])
        
        with col2:
            st.metric("Total Dribbles", events_info["total_dribbles"])
            
        with col3:
            st.metric("Total Shots", events_info["total_shots"])
            
        with col4:
            st.metric("Total Duels", events_info["total_duels"])
            
        st.divider()
 
        st.markdown(f"<h3 style='text-align: center;'>Passes</h3>", unsafe_allow_html=True)
        
        add_vertical_space(1)
        
        passes_events = self.get_cached_player_event(match_info, player_name, 'passes').reset_index()
        
        self.plot_player_passes(passes_events)
        
    def plot_team_shots(self, shot_events: DataFrame, shots_coords: DataFrame):
        pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='#c7d5cc', stripe=True)
        fig, ax = pitch.draw()
        
        kde = sns.kdeplot(
            x=shots_coords['x'],
            y=shots_coords['y'],
            fill=True,
            thresh=0.05,
            alpha = 0.7,
            n_levels=12,
            cmap = 'gnuplot'
        )
        
        for i in range(len(shot_events)):
            if shot_events.shot_outcome[i]=='Goal':
                pitch.arrows(shot_events.location[i][0], shot_events.location[i][1], shot_events.shot_end_location[i][0], shot_events.shot_end_location[i][1], ax=ax, color='green', width=3)
                pitch.scatter(shot_events.location[i][0], shot_events.location[i][1], ax = ax, color='green', alpha=1)
            elif shot_events.shot_outcome[i] in ['Blocked', 'Saved']:
                pitch.arrows(shot_events.location[i][0], shot_events.location[i][1], shot_events.shot_end_location[i][0], shot_events.shot_end_location[i][1], ax=ax, color='red', width=3)
                pitch.scatter(shot_events.location[i][0], shot_events.location[i][1], ax = ax, color='red', alpha=1)
            else:
                pitch.arrows(shot_events.location[i][0], shot_events.location[i][1], shot_events.shot_end_location[i][0], shot_events.shot_end_location[i][1], ax=ax, color='orange', width=3)
                pitch.scatter(shot_events.location[i][0], shot_events.location[i][1], ax = ax, color='orange', alpha=1)

        st.pyplot(fig)
        
        st.markdown("""
            <style>
            .legend-box {
                display: flex;
                align-items: center;
                margin-bottom: 5px;
            }
            .legend-color {
                width: 20px;
                height: 20px;
                margin-right: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

        legend_html = """
            <div class="legend-box">
                <div class="legend-color" style="background-color: green;"></div>
                <span>Goal</span>
            </div>
            <div class="legend-box">
                <div class="legend-color" style="background-color: red;"></div>
                <span>Blocked/Saved</span>
            </div>
            <div class="legend-box">
                <div class="legend-color" style="background-color: orange;"></div>
                <span>Other</span>
            </div>
        """
        
        st.markdown(legend_html, unsafe_allow_html=True)
        
    def plot_player_passes(self, passes_events):
        coords = passes_events['location']
        coords = pd.DataFrame(coords.to_list(), columns=['x', 'y'])
        
        pitch = Pitch(pitch_type='statsbomb', pitch_color='grass', line_color='#c7d5cc', stripe=True)
        fig, ax = pitch.draw()

        kde = sns.kdeplot(
            x=coords['x'],
            y=coords['y'],
            fill=True,
            thresh=0.05,
            alpha = 0.5,
            n_levels=12,
            cmap = 'gnuplot'
        )

        for i in range(len(passes_events)):
            if passes_events.pass_outcome[i]=='Incomplete' or passes_events.pass_outcome[i]=='Unknown':
                plt.plot((passes_events.location[i][0], passes_events.pass_end_location[i][0]), (passes_events.location[i][1], passes_events.pass_end_location[i][1]), color='red')
                plt.scatter(passes_events.location[i][0], passes_events.location[i][1], color='red')
            elif passes_events.pass_outcome[i]=='Pass Offside':
                plt.plot((passes_events.location[i][0], passes_events.pass_end_location[i][0]), (passes_events.location[i][1], passes_events.pass_end_location[i][1]), color='blue')
                plt.scatter(passes_events.location[i][0], passes_events.location[i][1], color='blue')
            elif passes_events.pass_outcome[i]=='Out':
                plt.plot((passes_events.location[i][0], passes_events.pass_end_location[i][0]), (passes_events.location[i][1], passes_events.pass_end_location[i][1]), color='yellow')
                plt.scatter(passes_events.location[i][0], passes_events.location[i][1], color='yellow')
            else:
                plt.plot((passes_events.location[i][0], passes_events.pass_end_location[i][0]), (passes_events.location[i][1], passes_events.pass_end_location[i][1]), color='black')
                plt.scatter(passes_events.location[i][0], passes_events.location[i][1], color='black')
        
        st.pyplot(fig)
        
        st.markdown("""
            <style>
            .legend-box {
                display: flex;
                align-items: center;
                margin-bottom: 5px;
            }
            .legend-color {
                width: 20px;
                height: 20px;
                margin-right: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        legend_html = """
            <div class="legend-box">
                <div class="legend-color" style="background-color: red;"></div>
                <span>Incomplete/Unknown</span>
            </div>
            <div class="legend-box">
                <div class="legend-color" style="background-color: blue;"></div>
                <span>Pass Offside</span>
            </div>
            <div class="legend-box">
                <div class="legend-color" style="background-color: yellow;"></div>
                <span>Out</span>
            </div>
            <div class="legend-box">
                <div class="legend-color" style="background-color: black;"></div>
                <span>Complete</span>
            </div>
        """
        st.markdown(legend_html, unsafe_allow_html=True)