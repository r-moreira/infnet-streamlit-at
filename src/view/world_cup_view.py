from view.abstract_view_strategy import AbstractViewStrategy, ViewStrategy
import streamlit as st

class WorldCupView(AbstractViewStrategy):
    
    def accept(self, view_strategy: ViewStrategy) -> bool:
        return view_strategy == ViewStrategy.WORLD_CUP
    
    def render(self) -> None:
        st.title("World Cup Analysis")
        st.write("This page provides an analysis of the FIFA World Cup from 1930 to 2014.")
        st.write("Select the 'Home' option in the sidebar to return to the home page.")
        st.write("Enjoy!")