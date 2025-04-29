from typing import Type

from sqlalchemy.orm import Session

from booking_service.infrastructure.persistence.models.orm_booking import Booking


class BookingRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, booking: Booking) -> Booking:
        db_booking = Booking(
            guest_name=booking.guest_name,
            guest_email=booking.guest_email,
            room_id=booking.room_id,
            check_in=booking.check_in,
            check_out=booking.check_out,
            total_cost=booking.total_cost,
            number_of_guests=booking.number_of_guests,
            status=booking.status,
            meal_reserved=booking.meal_reserved,  # Added meal_reserved field
        )
        self.session.add(db_booking)
        self.session.commit()
        self.session.refresh(db_booking)
        return db_booking

    def get(self, booking_id: int) -> Booking | None:
        booking = self.session.query(Booking).filter(int(Booking.id) == booking_id).first()
        return booking

    def list_all(self) -> list[Type[Booking]]:
        return self.session.query(Booking).all()

