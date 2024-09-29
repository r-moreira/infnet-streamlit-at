from abc import ABC, abstractmethod

from view.abstract_streamlit_view import AbstractStreamlitView

from enum import Enum

class ViewStrategy(Enum):
    HOME = "Home"
    WORLD_CUP = "World Cup"

class AbstractViewStrategy(AbstractStreamlitView):
    
    @abstractmethod
    def accept(self, view_strategy: ViewStrategy) -> bool:
        pass