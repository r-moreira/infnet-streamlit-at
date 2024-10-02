from typing import List
from repository.statsbomb_repository import StatsBombRepository
from service.session_state_service import SessionStateService
from view.abstract_statsbomb_view import AbstractStatsBombView
from view.abstract_view_strategy import ViewStrategy


class NationalCompetitionsView(AbstractStatsBombView):
    
    def __init__(
            self,
            statsbomb_repository: StatsBombRepository,
            session_state_service: SessionStateService
        ) -> None:
        super().__init__(statsbomb_repository, session_state_service)
        
    def get_title(self) -> str:
        return "National Competitions"
    
    def accept(self, view_strategy: ViewStrategy) -> bool:
        return view_strategy == ViewStrategy.NATIONAL_COMPETITIONS
    
    def get_competitions_list(self) -> List[str]:
        return [
            'Bundesliga',
            'Copa del Rey',
            "FA Women's Super League",
            'Indian Super League',
            'La Liga',
            'Liga Profesional',
            'Ligue 1',
            'Major League Soccer',
            'North American League',
            'NWSL',
            'Premier League',
            'Serie A'
        ]   