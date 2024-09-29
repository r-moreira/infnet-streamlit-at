from abc import ABC, abstractmethod
from typing import Any

class AbstractStreamlitView(ABC):
    
    @abstractmethod
    def render(self, *args: Any, **kwargs: Any) -> None | Any:
        pass