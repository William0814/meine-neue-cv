from flask import Flask, redirect, render_template, request, flash, url_for
from flask_mail import Mail    
from classes.mailTasks import send_email_async
from percistence.form import Form, db
from datetime import datetime
from classes.emailSender import GmailSmtpEmailSender
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from classes.tolgge import TolggeManager

load_dotenv()
app = Flask(__name__)

tolgge = TolggeManager(
    api_key =os.getenv('TOLGEE_API_KEY'),
    default_lang= 'en-US'
)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = app.config["MAIL_USERNAME"]

app.config["MAIL_TIMEOUT"] = 10

mail = Mail(app)
db.init_app(app)

@app.context_processor
def inject_url_for_lang():
    from flask import url_for

    def url_for_lang(endpoint, **values):
        lang = request.args.get('lang', 'en-US')
        if lang:
            values['lang'] = lang
        return url_for(endpoint, **values)
    return dict(url_for_lang=url_for_lang)

@app.route("/", methods=['GET', 'POST'])
def home():
    lang = request.args.get('lang', 'en-US')
    context = tolgge.get_translation(lang)

    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        message = request.form['message'].strip()
        date = datetime.now()

        form =  Form(name=name, email=email, message=message, date=date)
        db.session.add(form)
        db.session.commit()

        message_body = (
        f"Name: {name}.\n"
        f"email: {email}.\n"
        f"message: {message}"
        )
        
        email_sender = GmailSmtpEmailSender(mail)
        send_email_async(
            flask_app=app,
            email_sender= email_sender,
            subject="New Message from your CV!!",
            body=message_body,
            recipients=[app.config['MAIL_USERNAME']]
        ) 

        flash(f"Hi {name}, your message has been sent successfully!", "success")
        return redirect(url_for('home', lang=lang))
    
    return render_template('index.html', **context)

    

@app.route('/about_me') 
def about_me():
    lang = request.args.get('lang', 'en-US')
    return render_template('aboutMe.html', **tolgge.get_translation(lang))

@app.route('/studies')
def studies():
    lang = request.args.get('lang', 'en-US')
    return render_template('studies.html', **tolgge.get_translation(lang))

@app.route('/experience')
def experience():
    lang = request.args.get('lang', 'en-US')
    return render_template('experience.html', **tolgge.get_translation(lang))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)