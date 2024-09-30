from abc import ABC, abstractmethod
from enums.view_strategy import ViewStrategy

class AbstractViewStrategy(ABC):
    
    @abstractmethod
    def accept(self, view_strategy: ViewStrategy) -> bool:
        pass