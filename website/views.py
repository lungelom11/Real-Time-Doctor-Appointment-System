from flask import Blueprint, render_template, request,redirect, url_for, flash, session
from .models import Patients, Appointments
from . import db
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")



@views.route("/appointment", methods=["GET","POST"])
@login_required
def appointment():
    if request.method == "POST":
        patient_id = current_user.id 
        branch = request.form.get("branch")
        date = request.form.get("date")
        time = request.form.get("time")

        appointment = Appointments.query.filter_by(patient_id=patient_id).first()
        if appointment:
            flash("Appointment already exists!", category="error")
            return redirect(url_for("views.viewAppointment"))
        
        new_appointment = Appointments(patient_id=patient_id, branch=branch, date=date, time=time)
        db.session.add(new_appointment)
        db.session.commit()
        flash("Appointment created!", category="success")
        return redirect(url_for("views.viewAppointment"))
        
    return render_template("appointment.html", current=current_user)

@views.route("/admin-area")
def adminArea():
    return render_template("admin-area.html")

@views.route("/patient-info")    
def patientInfo():
    return render_template("patient.html", current= current_user)

@views.route("/view-appointment")    
def viewAppointment():
    return render_template("view-appointment.html", current= current_user)    

@views.route("/admin", methods=["GET","POST"])
@login_required
def admin():
    patients = Patients.query.all()
    return render_template("admin.html", patients = patients,current=current_user)

@views.route("/schedule")    
def schedule():
    return render_template("schedule.html", current= current_user) 

@views.route("/update", methods=["GET","POST"])
def update():
    
    if request.method == "POST":
        patient_info = Patients.query.get(request.form.get("id"))

        patient_info.email = request.form["email"]
        patient_info.firstname = request.form["firstname"]
        patient_info.lastname = request.form["lastname"]
        patient_info.password = generate_password_hash(request.form["password"])
        patient_info.contact_no = request.form["contact_no"]

        db.session.commit()

        flash("User Successfully Updated", category="success")

        return redirect(url_for("views.admin"))

@views.route("/delete/<int:id>")
def delete(id):
    delete_patient = Patients.query.get(id)
    db.session.delete(delete_patient)
    db.session.commit()
    flash("Patient Successfully Deleted", category="success")
    return redirect(url_for("views.admin"))

@views.route("doctor-dashboard")
def doctorDashboard():
    return render_template("doctor-dashboard.html")