from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from view.main_view import MainView

class Container(containers.DeclarativeContainer):    
    main_view = providers.Singleton(
        MainView
    )

@inject
def main(main_view: MainView = Provide[Container.main_view]) -> None:
    main_view.render()


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    main()