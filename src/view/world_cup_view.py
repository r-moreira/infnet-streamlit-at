from repository.statsbomb_repository import StatsBombRepository
from service.session_state_service import SessionStateService
from view.abstract_view_strategy import AbstractViewStrategy, ViewStrategy
import streamlit as st
from streamlit_option_menu import option_menu

class WorldCupView(AbstractViewStrategy):
    def __init__(
            self,
            statsbomb_repository: StatsBombRepository,
            session_state_service: SessionStateService
        ) -> None:
        
        self.statsbomb_repository = statsbomb_repository
        self.session_state_service = session_state_service
    
    def accept(self, view_strategy: ViewStrategy) -> bool:
        return view_strategy == ViewStrategy.WORLD_CUP
    
    def render(self) -> None:
        st.title("World Cup Analysis")
        
        menu_option = option_menu(
            None, 
            options=["Team", "Match", "Player"], 
            icons=['house', 'cloud-upload', "list-task"], 
            menu_icon="cast",
            default_index=0, 
            orientation="horizontal"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            competitions = self.statsbomb_repository.get_competitions()
            
            competition_name = st.selectbox(
                "Competition",
                competitions["competition_name"].unique()
            )
        
        with col2:
            competition = self.statsbomb_repository.get_competition(competition_name)
            
            season_name = st.selectbox(
                "Season",
                competition["season_name"].unique()
            )
            
            
        matches = self.statsbomb_repository.get_matches(competition_name, season_name)
        
        team_name = st.selectbox(
            "Team Name",
            matches["home_team"].unique()
        )
        
        team_matches = self.statsbomb_repository.get_team_matches(competition_name, season_name, team_name)
        
        if menu_option == "Team":
            #self.team_fragment(competition_name, season_name)
            st.write("In Progress")
        elif menu_option == "Match":
            self.match_fragment(team_matches)
        elif menu_option == "Player":
            st.write("In Progress")

    def match_fragment(self, team_matches):
        
        
        team_match_option = st.selectbox(
            "Match",
            team_matches["match_option"].unique()
        )

        match_info = self.statsbomb_repository.get_team_match(team_matches, team_match_option)
        
        with st.expander("Match Info"):
            st.write(match_info)
        
        st.dataframe(team_matches)
     
        