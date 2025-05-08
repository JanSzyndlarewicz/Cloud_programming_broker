from fastapi import APIRouter, Depends
from app.api.controllers import EmailController
from app.commands.create_invoice_command import SendEmailCommand
from app.commands.create_invoice_command_handler import SendEmailCommandHandler
from app.events.email_sent_event_publisher import EmailSentEventPublisher
from app.queries.get_email_by_invoice_id_query_handler import GetEmailByInvoiceIdQueryHandler
from app.queries.get_emails_by_mail_recipients_query_handler import (
    GetEmailsByMailRecipientQueryHandler,
)
from app.queries.get_emails_query_handler import GetEmailsQueryHandler
from app.services.email_service import EmailService
from infrastructure.config.settings import Config
from infrastructure.messaging.event_bus import RabbitMQEventBus
from infrastructure.persistence import get_db
from infrastructure.persistence.repositories.email_log_repository import EmailLogRepository
from sqlalchemy.orm import Session

router = APIRouter()


def get_email_controller(db: Session = Depends(get_db)):
    email_log_repository = EmailLogRepository(db)
    email_service = EmailService(
        Config.SMTP_SERVER,
        Config.SMTP_PORT,
        Config.SMTP_USERNAME,
        Config.SMTP_PASSWORD,
    )
    event_bus = RabbitMQEventBus()
    event_publisher = EmailSentEventPublisher(event_bus)
    send_email_command_handler = SendEmailCommandHandler(
        email_service=email_service,
        email_log_repository=email_log_repository,
        event_publisher=event_publisher,
    )
    get_email_by_invoice_id_query_handler = GetEmailByInvoiceIdQueryHandler(email_log_repository)
    get_emails_by_mail_recipient_query_handler = GetEmailsByMailRecipientQueryHandler(email_log_repository)
    get_emails_query_handler = GetEmailsQueryHandler(email_log_repository)
    return EmailController(
        send_email_command_handler=send_email_command_handler,
        get_email_by_invoice_id_query_handler=get_email_by_invoice_id_query_handler,
        get_emails_by_mail_recipient_query_handler=get_emails_by_mail_recipient_query_handler,
        get_emails_query_handler=get_emails_query_handler,
    )


@router.post("/emails/send")
async def send_email(command: SendEmailCommand, controller: EmailController = Depends(get_email_controller)):
    return await controller.send_email(command)


@router.get("/emails/invoices/{invoice_id}")
async def get_email_by_invoice_id(invoice_id: int, controller: EmailController = Depends(get_email_controller)):
    return await controller.get_email_by_invoice_id(invoice_id)


@router.get("/emails/recipient")
async def get_emails_by_recipient(recipient_email: str, controller: EmailController = Depends(get_email_controller)):
    return await controller.get_emails_by_recipient(recipient_email)


@router.get("/emails")
async def get_all_emails(controller: EmailController = Depends(get_email_controller)):
    return await controller.get_all_emails()
