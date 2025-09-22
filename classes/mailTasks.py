from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from flask import Flask, current_app
from .emailSender import SendenEmail


_executor = ThreadPoolExecutor(max_workers=2)
def send_email_async(flask_app: Flask, email_sender: SendenEmail, subject: str, body: str, recipients: List[str], sender: Optional[str] = None) -> None:
    
    def _task():
        try:
            with flask_app.app_context():
                flask_app.logger.info("Sending email to %s ...", recipients)
                email_sender.Send(subject, body, recipients, sender=sender)
                flask_app.logger.info("Email sent successfully")
        except Exception:
                flask_app.logger.exception("Failed to log email sending error")
    
    _executor.submit(_task)