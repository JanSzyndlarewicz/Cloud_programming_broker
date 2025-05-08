from decimal import Decimal

from infrastructure.persistence.repositories.booking_repository import BookingRepository
from fastapi import HTTPException


class GetBookingQueryHandler:
    def __init__(self, booking_repository: BookingRepository):
        self.booking_repository = booking_repository

    def handle(self, booking_id: int) -> dict[str, int | str | Decimal | float]:
        booking = self.booking_repository.get(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return {
            "id": booking.id,
            "guest_name": booking.guest_name,
            "guest_email": booking.guest_email,
            "room_id": booking.room_id,
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "total_cost": booking.total_cost,
            "status": booking.status,
        }
