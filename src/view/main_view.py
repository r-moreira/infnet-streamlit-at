import logging
from typing import List
import streamlit as st
from enums.view_strategy import ViewStrategy
from view.abstract_streamlit_view import AbstractStreamlitView
from view.abstract_view_strategy import AbstractViewStrategy

class MainView(AbstractStreamlitView):
    logger = logging.getLogger(__name__)
    
    def __init__(
            self,
            sidebar_view: AbstractStreamlitView,
            view_strategy_list: List[AbstractViewStrategy],
        ) -> None:
        self.sidebar_view = sidebar_view
        self.view_strategy_list = view_strategy_list
     
    @st.dialog("Error")
    def global_error_dialog(self) -> None:
        st.error(f"Something went wrong :(")
        
    def render(self) -> None:
        try:
            self.do_render()
        except Exception as e:
            logging.error(f"Error rendering View: {e}")
            self.global_error_dialog()

    def do_render(self):
        st.set_page_config(
            page_title="Soccer Analysis App",
            page_icon="⚽",
            layout="centered",
        )
        
        sidebar_option: ViewStrategy = self.sidebar_view.render()
        
        MainView.logger.info(f"Sidebar option selected: {sidebar_option}")
        
        # Render the view based on the sidebar option @Strategy Pattern
        for view_strategy in self.view_strategy_list:
            if view_strategy.accept(sidebar_option):
                MainView.logger.info(f"Rendering view strategy: {view_strategy}")
                view_strategy.render()
                break