from . import db
from flask_login import UserMixin

class Patients(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    password = db.Column(db.String(150))
    contact_no = db.Column(db.String(50))
    appointment = db.relationship("Appointments")

    def __init__(self, email, firstname, lastname, password, contact_no):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.contact_no = contact_no


class Appointments(db.Model, UserMixin):
    appointment_id = db.Column(db.String(100), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))
    branch = db.Column(db.String(100))
    date = db.Column(db.Date)
    time = db.Column(db.String(10))

    def __init__(self, patient_id, branch, date, time):
        self.patient_id = patient_id
        self.branch = branch
        self.date = date
        self.time = time
