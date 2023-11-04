from flask import Blueprint, render_template, request,redirect, url_for, flash, session
from .models import Doctor
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user


doc = Blueprint("doc", __name__)


@doc.route("/register-doctor", methods=["GET","POST"])
def registerDoctor():
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

@doc.route("/login-doctor", methods=["GET","POST"])
def loginDoctor():
    if request.method =="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        doctor = Doctor.query.filter_by(email=email).first()
        if Doctor:
            if check_password_hash(doctor.password, password):
                    flash("Logged in successfully", category="success")  
                    login_user(doctor, remember=True) 
                    return redirect(url_for("doc.doctorHome"))
            else:
                flash("Incorrect Password, please try again", category="error")
                return render_template("admin-area.html")
        else:
            flash("Email does not exist!", category="error")
            return redirect(url_for(views.adminArea))

    return render_template("doctor-home.html", doc=current_user)


@doc.route("/doctor/home")
@login_required
def doctorHome():
    return render_template("doctor-home.html", doc=current_user)