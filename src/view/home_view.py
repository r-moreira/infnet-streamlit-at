from view.abstract_view_strategy import AbstractViewStrategy, ViewStrategy
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

class HomeView(AbstractViewStrategy):
    def accept(self, view_strategy: ViewStrategy) -> bool:
        return view_strategy == ViewStrategy.HOME

    def render(self) -> None:
        st.title("Welcome!")
        
        add_vertical_space(2)
        
        st.image("image/fireball.png", width=500)
        
        st.markdown("""
        <style>
        .soccer-theme {
            font-size: 18px;
            color: #2E8B57;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("Explore a wide range of soccer competitions, matches, and player information. Dive into detailed statistics and analysis to enhance your understanding of the beautiful game")
        
        add_vertical_space(2)
        
        st.markdown("Stay updated with the latest soccer news and trends. Enjoy your journey through the world of soccer!")

        add_vertical_space(2)
        
        st.markdown("Select a menu item on the left to begin")