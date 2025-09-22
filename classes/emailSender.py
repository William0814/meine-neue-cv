from flask_mail import Mail, Message
import os
from abc import ABC, abstractmethod
from typing import List, Optional
from flask import current_app as app

class SendenEmail(ABC):
    @abstractmethod
    def Send(self, subject: str, body: str, recipients: List[str], sender: Optional[str] = None) -> None:
        ...


class GmailSmtpEmailSender(SendenEmail):
    def __init__(self, mail: Mail):
        self.mail = mail

    def Send(self, subject: str, body: str, recipients: List[str], sender: Optional[str] = None) -> None:

        _sender = sender or app.config.get('MAIL_USERNAME') or app.config.get('MAIL_DEFAULT_SENDER')
        message = Message(subject=subject, sender=_sender, recipients=recipients, body=body)
        self.mail.send(message)




    # def email_config(app, msg):
    #     app.config["MAIL_SERVER"] = "smtp.gmail.com"
    #     app.config["MAIL_PORT"] = 465
    #     app.config["MAIL_USE_SSL"] = True
    #     app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    #     app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

    #     mail = Mail(app)

    #     message = Message(subject= "New Message of your CV!!",
    #                     sender=app.config['MAIL_USERNAME'],
    #                     recipients=[app.config['MAIL_USERNAME']],
    #                     body=msg)
    #     mail.send(message)
    