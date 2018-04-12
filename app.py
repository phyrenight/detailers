from flask import Flask, render_template, request, session, redirect, url_for
from flask import flash
from flask.ext.bctypt import Bcrypt
from flask_mail import Mail, Message
from database import User, Vehicle, Appointments, VehicleImages
from config import mail_server, mail_port, mail_username, mail_password, \
                   secret_key  # 

app = Flask(__name__)
bcrypt = Bcrypt

app.config['MAIL_SERVER'] = mail_server
app.config['MAIL_PORT'] = mail_port
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


app.secret_key = secret_key

mail = Mail(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    return 'signup'


@app.route('/login', methods=['GET', 'POST'])
def login():
    return 'login'


@app.route('/logout')
def logout():
    if 'email' in session:
        session.clear()
        flash('You have been logged out')
        return redirect(url_for('home'))
    else:
        flash('You are not currently logged in')
    return render_template('home.html')


@app.route('/createAppointment', methods=['GET', 'POST'])
def create_appointment():
    return 'create_appointment'


@app.route('/view_appointments')
def view_appointments():
    return 'view_appointments'


@app.route('/view_appointment')
def view_appointment():
    return 'view_appointment'


@app.route('/cancelAppointment')
def cancel_appointment():
    return 'cancel_appointment'


@app.route('/assignjob')
def assign_job():
    return 'assign_job'


@app.route('/add_employee' methods=['GET', 'POST'])
def add_employee():
    return 'add_employee'


@app.errorhandler(500)
def internal_error(error):
    return render_template('internal500.html')


@app.errorhandler(404)
def file_not_found(error):
    return render_template('error404.html')


if __name__ == "__main__":
    app.run(debug=True)
