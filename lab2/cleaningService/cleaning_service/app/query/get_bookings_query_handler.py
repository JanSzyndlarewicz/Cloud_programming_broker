from cleaning_service.infrastructure.database.repositories import BookingRepository
from sqlalchemy.orm import InstrumentedAttribute


class GetBookingsQueryHandler:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def handle(self) -> list[dict[str, InstrumentedAttribute]]:
        bookings = self.booking_repository.list_all()
        return [
            {
                "id": booking.id,
                "guest_name": booking.guest_name,
                "guest_email": booking.guest_email,
                "status": booking.status,
            }
            for booking in bookings
        ]
