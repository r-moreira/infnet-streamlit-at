import streamlit as st

from enums.statsbomb_view_menu_option import StatsBombViewMenuOption

class SessionStateService: 
    def __init__(self, states_prefix: str) -> None:
        self.states_prefix = states_prefix
        self.prefixed_view_menu_option = f'{self.states_prefix}_view_menu_option'
        
    def set_view_menu_option(self, menu_option: str) -> None:
        print(f"menu_option: {self.prefixed_view_menu_option}")
        if menu_option not in StatsBombViewMenuOption.to_value_list():
            raise ValueError(f"Invalid menu option: {menu_option}")

        st.session_state[self.prefixed_view_menu_option] = menu_option
        
    def get_view_menu_option(self) -> str:
        if self.prefixed_view_menu_option not in st.session_state:
            SessionStateService.set_view_menu_option(StatsBombViewMenuOption.TEAM.value)
        
        return st.session_state[self.prefixed_view_menu_option]

    def is_view_menu_option(self) -> bool:
        return self.prefixed_view_menu_option in st.session_state