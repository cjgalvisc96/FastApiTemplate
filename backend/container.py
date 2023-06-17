from dependency_injector import providers, containers

from backend.auctions import AuctionsContainer


class ApplicationContainer(containers.DeclarativeContainer):
    auctions_package = providers.Container(AuctionsContainer)
