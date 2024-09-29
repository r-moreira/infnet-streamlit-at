import logging
from typing import List
import streamlit as st
from view.abstract_streamlit_view import AbstractStreamlitView
from view.abstract_view_strategy import AbstractViewStrategy, ViewStrategy

class MainView(AbstractStreamlitView):
    logger = logging.getLogger(__name__)
    
    def __init__(
            self,
            sidebar_view: AbstractStreamlitView,
            view_strategy_list: List[AbstractViewStrategy],
        ) -> None:
        self.sidebar_view = sidebar_view
        self.view_strategy_list = view_strategy_list
        
    def render(self) -> None:
        st.set_page_config(
            page_title="World Cup App",
            page_icon="🌐",
            layout="wide",
        )
        
        sidebar_option: ViewStrategy = self.sidebar_view.render()
        
        MainView.logger.debug(f"Sidebar option selected: {sidebar_option}")
        
        # Render the view based on the sidebar option @Strategy Pattern
        for view_strategy in self.view_strategy_list:
            if view_strategy.accept(sidebar_option):
                MainView.logger.debug(f"Rendering view strategy: {view_strategy}")
                view_strategy.render()
                break