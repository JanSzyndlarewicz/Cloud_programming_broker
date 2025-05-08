from typing import Optional

from infrastructure.persistence.repositories.dining_reservation_repository import (
    DiningReservationRepository,
)


class GetDiningReservationsQueryHandler:
    def __init__(self, dining_repository: DiningReservationRepository):
        self.dining_repository = dining_repository

    def handle(self, guest_name: Optional[str] = None, reservation_date: Optional[str] = None,
               guest_email: Optional[str] = None) -> list:
        return self.dining_repository.list_all(
            guest_name=guest_name,
            reservation_date=reservation_date,
            guest_email=guest_email
        )
