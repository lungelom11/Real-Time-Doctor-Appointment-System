from flask import Blueprint, render_template, request,redirect, url_for, flash, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")



@views.route("/appointment", methods=["GET","POST"])
@login_required
def book():
    return render_template("appointment.html", current=current_user)

@views.route("patient-info")    
def patientInfo():
    return render_template("patient.html", current= current_user)

@views.route("/admin", methods=["GET","POST"])
@login_required
def admin():
    users = User.query.all()
    return render_template("admin.html", users = users,current=current_user)



@views.route("/update", methods=["GET","POST"])
def update():
    
    if request.method == "POST":
        user_data = User.query.get(request.form.get("id"))

        user_data.email = request.form["email"]
        user_data.firstname = request.form["firstname"]
        user_data.lastname = request.form["lastname"]
        user_data.password = request.form["password"]
        user_data.role = request.form["role"]

        db.session.commit()

        flash("User Successfully Updated", category="success")

        return redirect(url_for("views.admin"))

    

@views.route("/delete/<int:id>")
def delete(id):
    delete_user = User.query.get(id)
    db.session.delete(delete_user)
    db.session.commit()
    flash("User Deleted", category="success")
    return redirect(url_for("views.admin"))
