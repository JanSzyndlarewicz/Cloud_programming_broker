from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.adapters.user_repository import UserRepository
from app.core.user_usecase import UserUseCase
from app.domain.schemas import UserCreateDTO
from app.events.user_event_publisher import EventPublisher
from app.infrastructure.database import get_db
from app.infrastructure.message_broker import MessageBroker

router = APIRouter()

def get_user_use_case(db: Session = Depends(get_db)) -> UserUseCase:
    user_repository = UserRepository(db)
    event_publisher = EventPublisher(MessageBroker())
    return UserUseCase(user_repository, event_publisher)

@router.post("/users/")
def create_user(user_data: UserCreateDTO, user_use_case: UserUseCase = Depends(get_user_use_case)):
    try:
        user = user_use_case.create_user(user_data)
        return {"id": user.id, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
