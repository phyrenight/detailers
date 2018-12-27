from flask import flash, render_template, request, session, redirect, url_for
from app import app
from app import db
from flask.ext.bcrypt import Bcrypt
from flask_mail import Mail, Message
from app.models import Users, Appointments,Vehicle#, VehicleImages
from config import Config  #mail_server, mail_port, mail_username, mail_password, \
                   #secret_key  #
from app.forms import SignUpForm, LoginForm, PasswordResetForm, ChangePasswordForm
from app.forms import CreateAppointmentForm


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
            if Users.query.filter_by(email=form.email.data).first():
                flash('Email address already in use')
                return render_template('Signup.html', form=form)
            else:
                users = Users(form.first_name.data,
                             form.last_name.data,
                             form.email.data,
                             form.password.data)
                db.session.add(users)
                db.session.commit()
                session['email'] = form.email.data
                session['name'] = form.first_name.data
                return redirect(url_for('home'))

    elif request.method == 'GET':
        return render_template('Signup.html', form=form)

@app.route('/choose_login')
def main_login():
    if 'email' in session:
        flash("You are already logged in")
        return  redirect(url_for('home'))
    else:
        return render_template('mainlogin.html')


@app.route('/employee_login', methods=['GET', 'POST'])
def employee_login():
    form  = LoginForm()
    if 'email' in session:
        flash("You are already logged in ")
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            if form.validate() is False:
                flash("Please fill in the input")
                return render_template('employee_login.html', form=form)
            else:
                email = form.email.data
                password = form.password.data
                user = Users.query.filter_by(email=form.email.data).first()
                if user.verify_password(password) and user.employee:
                    session['email'] = form.email.data
                    session['name'] = user.first_name
                    session['id'] = user.id
                    return redirect(url_for('home'))
                else:
                   return redirect(url_for('login'))
        elif request.method == 'GET':
            return render_template('employee_login.html', form=form)


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
            user = Users.query.filter_by(email=form.email.data).first()
            if user.verify_password(password):
                session['email'] = form.email.data
                session['name'] = user.first_name
                session['id'] = user.id
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


@app.route('/add_marc')
def add_marc():
    if 'email' in session:
        return redirect(url_for('home'))
    else:
        users = Users('Marc',
                      'Preston',
                      'phyrenight@gmail.com',
                      'C@melB@ck@58',
                      True,
                      'Admin')
        db.session.add(users)
        db.session.commit()
        return render_template('home.html')

@app.route('/createappointment', methods=['GET', 'POST'])
def create_appointment():
    if 'email' not in session:
        #TODO: add flash to notify user that they must be logged in to make an appointment
        redirect(url_for('login'))
    form = CreateAppointmentForm()
    if request.method == 'GET':
        return render_template('create_appointment.html', form=form)
    elif request.method == 'POST':
        print session["email"]
        user = Users.query.filter_by(email=session['email']).first()
        print user.email
        appointment = Appointments(
            date=form.date.data,
            user_id=user.id)
        db.session.add(appointment)
        db.session.commit()
        return render_template('home.html')


@app.route('/profile/<user_id>')
def profile(user_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    user = Users.query.filter_by(id=user_id).first()
    if user == None:
        flash('User does not exist')
        return redirect(url_for('home'))
    elif user.email == session['email']:
        appointments = Appointments.query.filter_by(user_id=user.id)
        return render_template('profile.html', user=user, appointments=appointments)


@app.route('/<user_id>/viewappointments')
def view_appointments(user_id):
    """
        View all appointments
    """
    if 'email' not in session:
        redirect(url_for('login'))
    user = Users.query.filter_by(id=user_id).first()
    if user.email == session['email']:
        appointments = Appointments.query.filter_by(user_id=user_id)
        for i in appointments:
            print(i.date)
        return render_template('viewappointments.html', appointments=appointments)
    else:
        flash('Not current users info')
        return redirect(url_for('home'))


@app.route('/<user_id>/viewappointment/<appointment_id>')
def view_appointment(user_id, appointment_id):
    """
   #    View a singular appointment
    """
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        appointment = Appointments.query.filter_by(id=appointment_id).first()
        user = Users.query.filter_by(
            id=appointment.user_id).first()
        if user.email == session['email']:
            return render_template(
                'viewappointment.html',
                appointment=appointment,
                status="Unassigned",
                detailer=None)
        else:
            return redirect(url_for('home'))


@app.route('/<user_id>/cancelappointment/<appointment_id>', methods=['GET', 'POST'])
def cancel_appointment(user_id, appointment_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    appointment = Appointments.query.filter_by(id=appointment_id).first()
    user = Users.query.filter_by(email=str(session['email'])).first()
    if appointment == None:
        flash('Appointment not on file')
        return redirect(url_for('home'))
    if request.method == 'GET':
        if session['email']  == user.email or user.employee:
            return render_template("cancelappointment.html",
                                   appointment=appointment,
                                   user_id=user.id)
        else:
            flash("This is not your appointment")
            return redirect(url_for('home'))
    if request.method =='POST':
        if user.id == appointment.user_id:
            appointment.job_status = 'Cancelled'
            db.session.commit()
            flash('Appointment has been cancelled.')
            return redirect(url_for('home'))
        else:
            flash('This appointment is not yours.')
            return redirect(url_for('home'))


@app.route('/editappointment/<appointment_id>')
def edit_appointment(appointment_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    pass


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


@app.route('/viewemployee/<employee_id>')
def viewemployee(employee_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    employee = User.query.filter_by(id=employee_id).first()
    user = User.query.filter_by(email=session['email']).first()
    if user.employee_job == 'admin':
        if employee == None:
            flash('Employee does not exist')
            return redirect(url_for('home'))
        else:
            return render_template('viewemployee.html', employee=employee)
    else:
        flash('User not logged in as admin.')
        return redirect(url_for('home'))


@app.route('/assignjob/<appointment_id>', methods=['GET', 'POST'])
def assign_job(appointment_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    appointment = Appointments.query.filter_by(id=appointment_id).first()
    detailers = Users.query.filter_by(employee_job='detailers')
    user = Users.query.filter_by(email=session['email']).first()
    if user.employee_job == 'admin':
        if request.method == 'POST':
            return render_template('assignjob.html')
        elif request.method == 'GET':
            return  render_template('assignjob.html', appointment=appointment, detailers=detailers)
    else:
        flash("Please login as an admin to access this page")
        return redirect(url_for('home'))


@app.route('/viewjobs', methods=['GET'])
def view_jobs():
    if 'email' not in session:
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['email']).first()
    if user == None:
        flash("Employee does not exist")
        return redirect(url_for('home'))
    elif user.employee == True and user.employee_job =='admin':
        appointments = Appointments.query().all()
        return render_template('viewjobs.html', appointments=appointments)
    elif user.employee == True and user.employee_job == 'detaier':
        appointments = Appointments.query.filter_by(detailer)
        return render_template('viewjobs.html', appointments=appointments)
    else:
        flash('Page unavailable')
        return redirect(url_for('home'))


@app.route('/<user_id>/addemployee/', methods=['GET', 'POST'])
def add_employee(user_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    user = Users.query.filter_by(id=user_id).first()
    form = addEmployeeForm()
    if user.employee_job == 'admin':
        if request.method == 'GET':
            return render_template('add_employee.html', form=form)
        elif request.method == 'POST':
            employee = Users(
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.password.data,
                True,
                form.employee_job.data)
            db.session.add(employee)
            db.session.commit()
            flash("Employee added")
            return redirect(url_for('home'))
    else:
        flash("Please login as an admin to view this page")
        return redirect(url_for('home'))


@app.route('/<user_id>/changepassword', methods=['GET', 'POST'])
def change_password(user_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    user = Users.query.filter_by(id=user_id).first()
    form = ChangePasswordForm()
    if request.method == 'GET':
        return render_template('change_password.html', form=form)
    if request.method == 'POST':
        if(form.password.data):
            user.password = user.hash_password(form.password.data)
            db.session.commit()
            flash("Password has been changed")
            return redirect(url_for('home'))
        else:
            flash("Please enter a Password")
            return render_template('change_password.html', form=form)


@app.route('/<user_id>/fireemployee', methods=['POST'])
def fire_employee(user_id):
    pass


@app.errorhandler(500)
def internal_error(error):
    return render_template('internal500.html')


@app.errorhandler(404)
def file_not_found(error):
    return render_template('error404.html'), 404


@app.route('/legal')
def legal():
    return render_template('legal.html')

@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')


if __name__ == "__main__":
    app.run(debug=True)
