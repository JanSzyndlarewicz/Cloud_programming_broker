import logging

logger = logging.getLogger(__name__)


class EmailService:
    def send_email(self, recipient: str, subject: str, body: str):
        # Simulate sending an email
        logger.info(f"[MOCKUP] Sending email to {recipient} with subject '{subject}'")
        # Add actual email-sending logic here (e.g., using SMTP or an email API)
        return True