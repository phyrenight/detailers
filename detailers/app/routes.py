from flask import flash, render_template, request, session, redirect, url_for
from app import app
from app import db
from flask.ext.bcrypt import Bcrypt
from flask_mail import Mail, Message
from app.models import Users, Appointments,Vehicle#, VehicleImages
from config import Config  #mail_server, mail_port, mail_username, mail_password, \
                   #secret_key  # 
from app.forms import SignUpForm, LoginForm, PasswordResetForm, ChangePassword
from app.forms import CreateAppointmentForm

#bcrypt = Bcrypt(app)
db.create_all()
app.config['MAIL_SERVER'] = Config.mail_server
app.config['MAIL_PORT'] = Config.mail_port
app.config['MAIL_USERNAME'] = Config.mail_username
app.config['MAIL_PASSWORD'] = Config.mail_password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)


@app.route('/')
@app.route('/home')
@app.route('/home/<user_id>')
def home():
    return render_template('home.html')


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if 'email' in session:
        return redirect(url_for('home'))
    form = SignUpForm()
    email = str(form.email.data)
    if request.method == 'POST':
        print form.email.data
        if form.validate() is False:
            flash('Please fill out the form completely')
            return render_template('Signup.html', form=form)
        else:
            if db.session.query(Users).filter_by(email=email).first():
                #User.query.filter_by(email=form.email.data).first():
                flash('Email address already in use')
                return render_template('Signup.html', form=form)
            else:
                pw_hash = bcrypt.generate_password_hash(str(form.password.data))
                users = User(first_name = form.first_name.data,
                             last_name = form.last_name.data,
                             email = form.email.data,
                             password = pw_hash)
                db.session.add(users)
               # db.session.commit()
                session['email'] = form.email.data
                session['name'] = form.first_name.data
                return redirect(url_for('home'))
            
    elif request.method == 'GET':
        return render_template('Signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        if form.validate() is False:
            return render_template('login.html', form=form)
        else:
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user is not None and bcrypt.check_password_hash(user.password,
                                                            password):
                print user.id
                session['email'] = form.email.data
                session['name'] = user.first_name
                return redirect(url_for('home'))
            else:
                return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'email' in session:
        session.clear()
        flash('You have been logged out')
        return redirect(url_for('home'))
    else:
        flash('You are not currently logged in')
    return render_template('home.html')


@app.route('/createappointment', methods=['GET', 'POST'])
def create_appointment():
    if 'email' not in session:
        redirect(url_for('login'))
    form = CreateAppointmentForm()
    if request.method == 'GET':
        return render_template('create_appointment.html', form=form)
    elif request.method == 'POST':
        user = User.query.filter_by(session['email']).first()
        appointment = Appointments(
            date=form.date.value,
            user_id=form.user_id.value)
        db.session.add(appointment)
        db.commit()
        return render_template('home')


@app.route('/profile/<user_id>')
def profile(user_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(id=user_id).first()
    if user.email == session['email']:
        return render_template('profile.html', user=user)


@app.route('/<user_id>/viewappointments')
def view_appointments(user_id):
    """
        View all appointments
    """
    if 'email' not in session:
        redirect(url_for('login'))
    user = User.query.filter_by(id=user_id).first()
    if user.email == session['email']:
        appointments = Appointments.query.filter_by(user_id=user_id)
        return render_template('viewappointments.html', appointments=appointments)
    else:
        flash('Not current users info')
        return redirect(url_for('home'))


@app.route('/<user_id>/view_appointment/<id>')
def view_appointment(user_id, id):
    """
   #    View a singular appointment
"""
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        appointment = Appointment.query.filter_by(id=id).first()
        user = User.query.filter_by(
            id=appointment.id).first()
        if user.email == session['email']:
            return render_template(
                'viewappointment.html',
                appointment=appointment,
                detailer=detailer)


@app.route('/<user_id>/cancelAppointment/<id>')
def cancel_appointment():
    if 'email' not in session:
        return redirect(url_for('login'))
    appointment = Appointment.query.filter_by(id=id).first()
    currentUser = User.query.filter_by(email=str(
        session['email'])).first()
    detailer = User.query.filter_by(
        id=appointment.detailer_assigned_id).first()
    customer = User.query.filter_by(
        id=appointment.customer_id).first()
    if appointment == None:
        flash('Appointment not on file')
        return redirect(url_for('home'))
    if request.method == 'GET':
        if session['email']  == customer.email or currentUser.status == 'admin':
            return render_template("cancelappointment.html", appointment=appointment) 
        else:
            flash("This is not your appointment")
            return redirect(url_for('home'))

    if request.method =='POST': 
        user = User.query.filter_by(email=str(session['email'])).first()
        appointment = Appointment.query.filter_by(id=id).first()
        if user.id == appointment.customer_id:
            appointment = Appointment()
            appointment.status = 'Cancel'
            db_session.commit()
            flash('Appointment has been cancelled.')
            return render_template('home.html')
        return 'cancel_appointment'


@app.route('/resetpassword', methods=['GET', 'POST'])
def reset_password():
    if 'email' in session:
        return redirect(url_for('home'))
    form = PasswordResetForm()
    if request.method == 'GET':
        return render_template('resetpassword.html', form=form)
    elif request.method == 'POST':
        if form.validte() is False:
            flash('Please enter a valid email')
            return render_template('resetpassword.html', form=form)
        else:
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None:
                msg = Message(
                    'Password reset',
                    sender=mail_username,
                    recipients=[form.email.data])
                msg.body = 'http://localhost:5000/changepassword'
                mail.send(msg)
                flash('Email sent to reset password')
                return redirect('home.html')
            else:
                flash('Email not in database')
                return render_template('resetpassword.html', form=form)


@app.route('/<user_id>/viewemployees')
def view_employees(user_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(id=user_id).first()
    if user.email == session['email'] and user.employee_job == 'admin':
        employees = User.query.filter_by(employee==True)
        return render_template('employeelist.html', employees=employees)


@app.route('/<user_id>/viewemployee')
def viewemployee(user_id):
    return 'views'

"""
@app.route('/assignjob', methods=['GET', 'POST'])
def assign_job():
    if 'email' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        employee = Employee.query.
        return render_template('assignjob.html')
    elif request.method == 'GET':
        return 'assign_job'


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'email' not in session:
        return redirect(url_for('login'))
    return 'add_employee'
"""


@app.errorhandler(500)
def internal_error(error):
    return render_template('internal500.html')


@app.errorhandler(404)
def file_not_found(error):
    return render_template('error404.html')


@app.route('/legal')
def legal():
    return 'legal'


if __name__ == "__main__":
    app.run(debug=True)
