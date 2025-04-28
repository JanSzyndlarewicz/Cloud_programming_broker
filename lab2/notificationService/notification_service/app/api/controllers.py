from fastapi import HTTPException
from notification_service.app.commands.create_invoice_command import SendEmailCommand
from notification_service.app.commands.create_invoice_command_handler import SendEmailCommandHandler
from notification_service.app.query.get_email_by_invoice_id_query_handler import GetEmailByInvoiceIdQueryHandler
from notification_service.app.query.get_emails_by_mail_recipients_query_handler import (
    GetEmailsByMailRecipientQueryHandler,
)
from notification_service.app.query.get_emails_query_handler import GetEmailsQueryHandler


class EmailController:
    def __init__(
        self,
        send_email_command_handler: SendEmailCommandHandler,
        get_email_by_invoice_id_query_handler: GetEmailByInvoiceIdQueryHandler,
        get_emails_by_mail_recipient_query_handler: GetEmailsByMailRecipientQueryHandler,
        get_emails_query_handler: GetEmailsQueryHandler,
    ):
        self.send_email_command_handler = send_email_command_handler
        self.get_email_by_invoice_id_query_handler = get_email_by_invoice_id_query_handler
        self.get_emails_by_mail_recipient_query_handler = get_emails_by_mail_recipient_query_handler
        self.get_emails_query_handler = get_emails_query_handler

    async def send_email(self, command: SendEmailCommand) -> dict:
        try:
            success = self.send_email_command_handler.handle(command)
            if success:
                return {"status": "email_sent"}
            else:
                raise HTTPException(status_code=500, detail="Failed to send email")
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_email_by_invoice_id(self, invoice_id: int):
        try:
            email_log = self.get_email_by_invoice_id_query_handler.handle(invoice_id)
            if not email_log:
                raise HTTPException(status_code=404, detail="Email not found for the given invoice ID")
            return email_log
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_emails_by_recipient(self, recipient_email: str):
        try:
            return self.get_emails_by_mail_recipient_query_handler.handle(recipient_email)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_all_emails(self):
        try:
            return self.get_emails_query_handler.handle()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
