from view.abstract_streamlit_view import AbstractStreamlitView
import streamlit as st
from streamlit_option_menu import option_menu

from view.abstract_view_strategy import ViewStrategy


class SidebarView(AbstractStreamlitView):
    
    def __init__(self) -> None:
        pass
    
    def render(self) -> ViewStrategy:
       with st.sidebar:
            selected: ViewStrategy = option_menu(
                "Main Menu", 
                options=[e.value for e in ViewStrategy], 
                icons=[
                    'house',
                    'globe2'
                ], 
                menu_icon="cast", 
                default_index=0
            )
            
            return ViewStrategy(selected)