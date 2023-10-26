from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                    flash("Logged in successfully", category="success") 
                    login_user(user, remember=True)   
                    return redirect(url_for("views.book"))
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
        role = request.form.get("role")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists!", category="error")

        elif len(email) < 4:
            flash("Email is too short.", category="error")

        elif len(password) < 5:
            flash("Password too short, must be at least 6 characters.", category="error")

        elif password != password2:
            flash("Passwords do not match, please enter again.", category="error")

        else:
            new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password), role=role)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category="success")
            login_user(new_user, remember=True)
            return redirect(url_for("views.admin"))
            
    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))