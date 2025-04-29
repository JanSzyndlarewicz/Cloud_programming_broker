import logging
from datetime import datetime
from typing import Optional

from booking_service.app.commands.create_booking_command import CreateBookingCommand
from booking_service.app.events.booking_created_event import BookingCreatedEventPublisher
from booking_service.domain.events.booking_created import BookingCreatedEvent
from booking_service.domain.models.booking import Booking, BookingStatus


from booking_service.infrastructure.persistence.models.orm_room import RoomStatus
from booking_service.infrastructure.persistence.repositories.booking_repository import BookingRepository
from booking_service.infrastructure.persistence.repositories.room_repository import RoomRepository

logger = logging.getLogger(__name__)


class CreateBookingCommandHandler:
    def __init__(
        self,
        booking_repository: BookingRepository,
        room_repository: RoomRepository,
        event_publisher: BookingCreatedEventPublisher,
    ):
        self.booking_repository = booking_repository
        self.room_repository = room_repository
        self.event_publisher = event_publisher

    def handle(self, command: CreateBookingCommand) -> Optional[int]:
        try:
            # Convert and validate dates
            check_in = datetime.strptime(command.check_in, "%Y-%m-%d").date()
            check_out = datetime.strptime(command.check_out, "%Y-%m-%d").date()

            if check_out <= check_in:
                raise ValueError("Check-out date must be after check-in date")

            # Get the room
            room = self.room_repository.get_room_by_id(command.room["room_id"])
            if not room:
                raise ValueError(f"Room {command.room['room_id']} not found")

            # Check availability using enum comparison
            if room.status.value != RoomStatus.available.value:
                raise ValueError(f"Room {room.number} is already booked")

            # Create booking
            booking = Booking(
                guest_name=command.guest_name,
                guest_email=command.guest_email,
                check_in=check_in,
                check_out=check_out,
                number_of_guests=command.number_of_guests,
                room_id=room.id,
                status=BookingStatus.pending,
            )
            booking.room = room  # Set the room relationship

            # Calculate cost
            booking.calculate_total_cost()

            # Update room status - use the enum value directly
            room.status = RoomStatus.booked.value

            # Save changes - ensure both objects are in session
            self.booking_repository.session.add(booking)
            self.booking_repository.session.add(room)  # Explicitly add room to session
            self.booking_repository.session.commit()
            self.booking_repository.session.refresh(booking)

            # Publish event
            event = BookingCreatedEvent(
                booking_id=booking.id,
                guest_name=booking.guest_name,
                guest_email=booking.guest_email,
                room_number=room.number,
                room_id=room.id,
                total_cost=booking.total_cost,
                number_of_guests=booking.number_of_guests,
                meal_reserved=command.meal_reserved,
                check_in=booking.check_in.isoformat(),
                check_out=booking.check_out.isoformat(),
                status=booking.status.value,
            )
            self.event_publisher.publish(event)

            return booking.id

        except Exception as e:
            logger.info(f"Booking failed: {str(e)}")
            self.booking_repository.session.rollback()
            raise
