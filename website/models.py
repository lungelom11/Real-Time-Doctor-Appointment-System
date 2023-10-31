from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    password = db.Column(db.String(150))
    contact_no = db.Column(db.String(50))

    def __init__(self, email, firstname, lastname, password, contact_no):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.contact_no = contact_no

class Doctor(db.Model, UserMixin):
    doctor_id = db.Column(db.String(100), primary_key=True)
    doc_firstname = db.Column(db.String(150))
    doc_lastname= db.Column(db.String(150))

    def __init__(self, doc_firstname, doc_lastname):
        self.doc_firstname = doc_firstname
        self.doc_lastname = doc_lastname
