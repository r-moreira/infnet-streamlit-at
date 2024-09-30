
from typing import List
from repository.statsbomb_repository import StatsBombRepository
from service.session_state_service import SessionStateService
from view.abstract_statsbomb_view import AbstractStatsBombView
from view.abstract_view_strategy import ViewStrategy


class CompetitionsView(AbstractStatsBombView):
    
    def __init__(
            self,
            statsbomb_repository: StatsBombRepository,
            session_state_service: SessionStateService
        ) -> None:
        super().__init__(statsbomb_repository, session_state_service)
        
    def get_title(self) -> str:
        return "Competitions Analysis"
    
    def accept(self, view_strategy: ViewStrategy) -> bool:
        return view_strategy == ViewStrategy.COMPETITIONS
    
    def get_competitions_list(self) -> List[str]:
        return [
            '1. Bundesliga',
            'African Cup of Nations',
            'Champions League',
            'Copa America',
            'Copa del Rey', 
            "FA Women's Super League",
            'Indian Super league',
            'La Liga', 
            'Liga Profesional',
            'Ligue 1',
            'Major League Soccer',
            'North American League', 
            'NWSL', 
            'Premier League',
            'Serie A',
            'UEFA Euro',
            'UEFA Europa League',
            "UEFA Women's Euro"
        ]   