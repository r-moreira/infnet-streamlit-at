from abc import ABC, abstractmethod
from enum import Enum

class ViewStrategy(Enum):
    HOME = "Home"
    WORLD_CUPS = "World Cups"
    COMPETITIONS = "Competitions"

class AbstractViewStrategy(ABC):
    
    @abstractmethod
    def accept(self, view_strategy: ViewStrategy) -> bool:
        pass