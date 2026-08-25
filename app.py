from flask import Flask, redirect, render_template, request, flash, url_for
from percistence.form import Form, db
from datetime import datetime
from classes.tolgge import TolggeManager
from threading import Thread
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- Config base ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db.init_app(app)
tolgge = TolggeManager(api_key=os.getenv('TOLGEE_API_KEY'), default_lang='en-US')

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL       = os.getenv("MAIL_FROM")     
TO_EMAIL         = os.getenv("MAIL_TO")  

def send_email_async(subject: str, body: str, reply_email: str):
    """Envía email por HTTP (SendGrid) en background; no bloquea el POST."""
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": FROM_EMAIL,
                "to": [TO_EMAIL],
                "subject": subject,
                "text": body,
                "reply_to": reply_email
            },
            timeout=10,
        )
        if not response.ok:
            app.logger.error(
                "Resend error %s: %s",
                response.status_code,
                response.text,
            )   
        response.raise_for_status()
    except requests.RequestException as e:
        app.logger.error("Failed to send email: %s", e)

@app.context_processor
def inject_url_for_lang():
    from flask import url_for
    def url_for_lang(endpoint, **values):
        lang = request.args.get('lang', 'en-US')
        if lang: values['lang'] = lang
        return url_for(endpoint, **values)
    return dict(url_for_lang=url_for_lang)

@app.route("/", methods=['GET', 'POST'])
def home():
    lang = request.args.get('lang', 'en-US')
    context = tolgge.get_translation(lang)

    if request.method == 'POST':
        name    = request.form['name'].strip()
        email   = request.form['email'].strip()
        message = request.form['message'].strip()
        date    = datetime.now()

        db.session.add(Form(name=name, email=email, message=message, date=date))
        db.session.commit()

        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        Thread(target=send_email_async,
               args=("New Message from your CV!!", body, email),
               daemon=True).start()

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
