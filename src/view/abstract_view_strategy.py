from abc import ABC, abstractmethod
from view.abstract_streamlit_view import AbstractStreamlitView
from enum import Enum

class ViewStrategy(Enum):
    HOME = "Home"
    WORLD_CUPS = "World Cups"
    COMPETITIONS = "Competitions"

class AbstractViewStrategy(AbstractStreamlitView):
    
    @abstractmethod
    def accept(self, view_strategy: ViewStrategy) -> bool:
        pass