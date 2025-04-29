from dining_service.app.api.controllers import DiningController
from dining_service.app.query.get_dining_reservations_query_handler import GetDiningReservationsQueryHandler

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dining_service.infrastructure.persistence import get_db
from dining_service.infrastructure.persistence.repositories.dining_reservation_repository import \
    DiningReservationRepository

router = APIRouter()


def get_dining_controller(db: Session = Depends(get_db)):
    dining_repository = DiningReservationRepository(db)
    return DiningController(GetDiningReservationsQueryHandler(dining_repository))


@router.get("/dining-reservations")
async def list_dining_reservations(controller: DiningController = Depends(get_dining_controller)):
    return await controller.get_dining_reservations()
