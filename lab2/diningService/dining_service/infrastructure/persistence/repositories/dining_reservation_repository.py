from typing import Type, Optional

from infrastructure.persistence.models.orm_dining_reservation import DiningReservation
from sqlalchemy.orm import Session


class DiningReservationRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, reservation: DiningReservation) -> DiningReservation:
        db_reservation = DiningReservation(
            guest_name=reservation.guest_name,
            guest_email=reservation.guest_email,
            reservation_date=reservation.reservation_date,
            number_of_guests=reservation.number_of_guests,
        )
        self.session.add(db_reservation)
        self.session.commit()
        self.session.refresh(db_reservation)
        return db_reservation

    def get(self, reservation_id: int) -> DiningReservation | None:
        return self.session.query(DiningReservation).filter(DiningReservation.id == reservation_id).first()

    def list_all(
            self,
            guest_name: Optional[str] = None,
            reservation_date: Optional[str] = None,
            guest_email: Optional[str] = None
    ) -> list[Type[DiningReservation]]:
        query = self.session.query(DiningReservation)

        if guest_name:
            query = query.filter(DiningReservation.guest_name == guest_name)
        if reservation_date:
            query = query.filter(DiningReservation.reservation_date == reservation_date)
        if guest_email:
            query = query.filter(DiningReservation.guest_email == guest_email)

        return query.all()
