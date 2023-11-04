from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Patients, Doctor
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_required, current_user, logout_user, login_user


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        patient = Patients.query.filter_by(email=email).first()
        if patient:
            if check_password_hash(patient.password, password):
                    flash("Logged in successfully", category="success") 
                    login_user(patient, remember=True)   
                    return redirect(url_for("views.appointment"))
            else:
                flash("Incorrect Password, please try again", category="error")
        else:
            flash("Email does not exist!", category="error")

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")
        password2 = request.form.get("confirm-password")
        contact_no = request.form.get("contact_no")

        patient = Patients.query.filter_by(email=email).first()
        if patient:
            flash("Email already exists!", category="error")

        elif len(email) < 4:
            flash("Email is too short.", category="error")

        elif len(password) < 5:
            flash("Password too short, must be at least 6 characters.", category="error")

        elif password != password2:
            flash("Passwords do not match, please enter again.", category="error")

        else:
            new_patient = Patients(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password), contact_no=contact_no)
            db.session.add(new_patient)
            db.session.commit()
            flash("Account created!", category="success")
            login_user(new_patient, remember=True)
            return redirect(url_for("views.appointment"))
            
    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        password = request.form.get("password")

        doctor = Doctor.query.filter_by(email=email).first()
        if doctor:
            flash("Doctor already exists!", category="error")

        elif len(email) < 4:
            flash("Email is too short.", category="error")

        elif len(password) < 5:
            flash("Password too short, must be at least 6 characters.", category="error")

        else:
            new_doctor = Doctor(firstname=firstname, lastname=lastname, email=email, password=generate_password_hash(password))
            db.session.add(new_doctor)
            db.session.commit()
            login_user(doctor, remember=True)
            flash("Account created!", category="success")
            return redirect(url_for("views.doctorDashboard"))
            
    return render_template("admin-area.html")