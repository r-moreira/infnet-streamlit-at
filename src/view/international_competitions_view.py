from typing import List
from repository.statsbomb_repository import StatsBombRepository
from service.session_state_service import SessionStateService
from view.abstract_statsbomb_view import AbstractStatsBombView
from view.abstract_view_strategy import ViewStrategy


class InternationalCompetitionsView(AbstractStatsBombView):
    
    def __init__(
            self,
            statsbomb_repository: StatsBombRepository,
            session_state_service: SessionStateService
        ) -> None:
        super().__init__(statsbomb_repository, session_state_service)
        
    def get_title(self) -> str:
        return "International Competitions"
    
    def accept(self, view_strategy: ViewStrategy) -> bool:
        return view_strategy == ViewStrategy.INTERNATIONAL_COMPETITIONS
    
    def get_competitions_list(self) -> List[str]:
        return [
            'African Cup of Nations',
            'Champions League',
            'Copa America',
            'UEFA Euro',
            'UEFA Europa League',
            "UEFA Women's Euro"
        ]