from view.abstract_view_strategy import AbstractViewStrategy, ViewStrategy
import streamlit as st

class HomeView(AbstractViewStrategy):
    def accept(self, view_strategy: ViewStrategy) -> bool:
        return view_strategy == ViewStrategy.HOME

    def render(self) -> None:
        st.title("Home")
        st.write("Welcome to the World Cup Analysis App!")
        st.write("This app provides an analysis of the FIFA World Cup from 1930 to 2014.")
        st.write("Use the sidebar to navigate through the app.")
        st.write("Select the 'World Cup Analysis' option to view the analysis.")
        st.write("Select the 'Home' option to return to this page.")
        st.write("Enjoy!")