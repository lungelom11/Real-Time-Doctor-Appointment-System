from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    password = db.Column(db.String(150))
    role = db.Column(db.String(50))

    def __init__(self, email, firstname, lastname, password, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.role = role
