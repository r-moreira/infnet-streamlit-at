import streamlit as st
from view.abstract_streamlit_view import AbstractStreamlitView

class MainView(AbstractStreamlitView):
    def __init__(self) -> None:
        pass
        
    def render(self) -> None:
        st.set_page_config(
            page_title="World Cup Analysis",
            page_icon="🌐",
            layout="wide",
        )
        
        st.title("World Cup Analysis")