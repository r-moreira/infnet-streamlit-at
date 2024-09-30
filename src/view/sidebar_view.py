from view.abstract_streamlit_view import AbstractStreamlitView
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.add_vertical_space import add_vertical_space
from view.abstract_view_strategy import ViewStrategy


class SidebarView(AbstractStreamlitView):
    
    def __init__(self) -> None:
        pass
    
    def render(self) -> ViewStrategy:
       with st.sidebar:
           
            add_vertical_space(4)
           
            st.title("⚽ Soccer Analysis APP")
           
            st.divider()
           
            add_vertical_space(1)
            
            selected: ViewStrategy = option_menu(
                "Main Menu", 
                options=[e.value for e in ViewStrategy], 
                icons=[
                    'house',
                    'globe2',
                    'trophy'
                ], 
                menu_icon="cast", 
                default_index=0
            )
            
            return ViewStrategy(selected)