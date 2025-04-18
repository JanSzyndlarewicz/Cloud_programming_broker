from sqlalchemy.orm import Session

from app.domain.schemas import UserCreateDTO
from app.domain.user import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user_data: UserCreateDTO) -> User:
        user = User(**user_data.model_dump())
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user