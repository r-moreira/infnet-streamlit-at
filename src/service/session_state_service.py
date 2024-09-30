import streamlit as st

from enums.statsbomb_view_menu_option import StatsBombViewMenuOption

class SessionStateService: 
    def __init__(self):
        pass
    
    @staticmethod
    def set_view_menu_option(menu_option: str) -> None:
        if menu_option not in StatsBombViewMenuOption.to_list():
            raise ValueError(f"Invalid menu option: {menu_option}")

        st.session_state['world_cups_view_menu_option'] = menu_option
        
    @staticmethod
    def get_view_menu_option() -> str:
        if 'world_cups_view_menu_option' not in st.session_state:
            SessionStateService.set_view_menu_option(StatsBombViewMenuOption.TEAM.value)
        
        return st.session_state['world_cups_view_menu_option']

    @staticmethod
    def is_view_menu_option() -> bool:
        return 'world_cups_view_menu_option' in st.session_state