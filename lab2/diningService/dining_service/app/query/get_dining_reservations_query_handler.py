from dining_service.infrastructure.database.repositories import DiningReservationRepository


class GetDiningReservationsQueryHandler:
    def __init__(self, dining_repository: DiningReservationRepository):
        self.dining_repository = dining_repository

    def handle(self) -> list:
        return self.dining_repository.list_all()
