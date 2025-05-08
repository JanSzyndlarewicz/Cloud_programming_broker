from datetime import datetime
from typing import Type

from infrastructure.persistence.models.orm_booking import Booking
from sqlalchemy.orm import Session


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
            meal_reserved=booking.meal_reserved,
        )
        self.session.add(db_booking)
        self.session.commit()
        self.session.refresh(db_booking)
        return db_booking

    def get(self, booking_id: int) -> Booking | None:
        booking = self.session.query(Booking).filter(Booking.id == booking_id).first()
        return booking

    def list_all(self) -> list[Type[Booking]]:
        return self.session.query(Booking).all()

    def get_overlapping_bookings(self, room_id: int, check_in: datetime.date, check_out: datetime.date):
        return self.session.query(Booking).filter(
            Booking.room_id == room_id,
            Booking.check_out > check_in,  # Booking ends after the requested check-in
            Booking.check_in < check_out  # Booking starts before the requested check-out
        ).all()
