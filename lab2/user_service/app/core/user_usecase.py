import logging
from time import sleep

from app.adapters.user_repository import UserRepository
from app.domain.schemas import UserCreateDTO
from app.events.user_event_publisher import EventPublisher


class UserUseCase:
    def __init__(self, user_repository: UserRepository, event_publisher: EventPublisher):
        self.logger = logging.getLogger(__name__)
        self.user_repository = user_repository
        self.event_publisher = event_publisher

    def create_user(self, user_data: UserCreateDTO):
        self.logger.debug("Creating user...")
        if not self._validate_user_data(user_data):
            raise ValueError("Invalid user data")

        user = self.user_repository.create(user_data)

        self.logger.debug("Waiting for 5 seconds...")
        sleep(5)

        self.logger.debug("User created")

        self.event_publisher.publish_user_created_event(user)

        return user

    def _validate_user_data(self, user_data: UserCreateDTO) -> bool:
        return True
