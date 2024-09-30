import logging
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from repository.statsbomb_repository import StatsBombRepository
from service.session_state_service import SessionStateService
from view.abstract_streamlit_view import AbstractStreamlitView
from view.competitions_view import CompetitionsView
from view.home_view import HomeView
from view.main_view import MainView
from view.sidebar_view import SidebarView
from view.word_cups_view import WordCupsView


class Container(containers.DeclarativeContainer):        
    session_state_service = providers.Singleton(SessionStateService)
    
    statsbomb_repository = providers.Singleton(StatsBombRepository)
    
    view_strategy_list = providers.List(   
        providers.Singleton(HomeView),
        providers.Singleton(
            WordCupsView,
            statsbomb_repository=statsbomb_repository,
            session_state_service=session_state_service
        ),
        providers.Singleton(
            CompetitionsView,
            statsbomb_repository=statsbomb_repository,
            session_state_service=session_state_service
        )
    )
    
    main_view = providers.Singleton(
        MainView,
        sidebar_view=providers.Singleton(SidebarView),
        view_strategy_list=view_strategy_list
    )

@inject
def main(main_view: AbstractStreamlitView = Provide[Container.main_view]) -> None:
    main_view.render()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    container = Container()
    container.wire(modules=[__name__])
    main()