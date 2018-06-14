from datetime import datetime
from app import db, bcrypt


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), index=True)
    last_name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(250), index=True, unique=True)
    password = db.Column(db.String(250))
    employee = db.Column(db.Boolean)
    employee_job = db.Column(db.String)
    appointments = db.relationship('Appointments', backref='owner_id', lazy='dynamic')
    vehicle = db.relationship('Vehicle', backref='customer_id', lazy='dynamic')

 
    def __init__(self, first_name, last_name, email, password, employee=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.employee = employee
        self.password = self.hash_password(password)


    def hash_password(self, password):
        return bcrypt.generate_password_hash(str(password))


class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    job_status = db.Column(db.String)


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    model = db.Column(db.String)
    make = db.Column(db.String)
    year = db.Column(db.Integer)
    color = db.Column(db.String)
    appointments = db.relationship('Appointments', backref='veh_id', lazy='dynamic')