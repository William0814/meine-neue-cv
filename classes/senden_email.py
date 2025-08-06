from flask_mail import Mail, Message


def email_config(app, msg):
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 465
    app.config["MAIL_USE_SSL"] = True
    app.config["MAIL_USERNAME"] = "correo.aplicaciones.ardit@gmail.com"
    app.config["MAIL_PASSWORD"] = "cyjw awse agna egda"

    mail = Mail(app)

    message = Message(subject= "New Message of your CV!!",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[app.config['MAIL_USERNAME']],
                      body=msg)
    mail.send(message)
    