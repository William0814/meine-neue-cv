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
        except Exception as e:
            try:
                flask_app.logger.exception(f"Failed to send email:", e)
            except Exception:
                print(f"Failed to send email: {str(e)}")

    _executor.submit(_task)