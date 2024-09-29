import logging
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from view.home_view import HomeView
from view.main_view import MainView
from view.sidebar_view import SidebarView
from view.world_cup_view import WorldCupView


class Container(containers.DeclarativeContainer):        
    view_strategy_list = providers.List(   
        providers.Singleton(HomeView),
        providers.Singleton(WorldCupView)
    )
    
    main_view = providers.Singleton(
        MainView,
        sidebar_view=providers.Singleton(SidebarView),
        view_strategy_list=view_strategy_list
    )

@inject
def main(main_view: MainView = Provide[Container.main_view]) -> None:
    main_view.render()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )
    container = Container()
    container.wire(modules=[__name__])
    main()