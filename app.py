from flask import Flask, render_template, request, flash    
from percistence.form import Form, db
from datetime import datetime
from classes.senden_email import email_config
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '0814082515ea&mi'

db.init_app(app)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        date = datetime.now()

        form =  Form(name=name, email=email, message=message, date=date)
        db.session.add(form)
        db.session.commit()

        message_body = (
        f"Name: {name}.\n"
        f"email: {email}.\n"
        f"message: {message}"
        )
        try:
            email_config(app, message_body)
            flash(f"Hi {name}, your message submitted succesfully!", "success")
        except Exception as e:
            flash(f"Error to email send: {str(e)}", "danger")

        return render_template("index.html")

    return render_template("index.html")

    

@app.route('/about_me')
def about_me():
    return render_template('aboutMe.html')

@app.route('/studies')
def studies():
    return render_template('studies.html')

@app.route('/experience')
def experience():
    return render_template('experience.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)