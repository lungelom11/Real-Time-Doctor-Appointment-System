from flask import Blueprint, render_template, request,redirect, url_for,flash
from flask_login import login_required, current_user
from .models import User
from . import db
from werkzeug.security import generate_password_hash

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/admin", methods=["GET","POST"])
def admin():
    users = User.query.all()
    return render_template("admin.html", users = users)


@views.route("/<int:id>/update", methods=["GET","POST"])
def update(id):
    update_user = User.query.filter_by(id = id).first()
    if request.method == "POST":
        if update_user:
            db.session.delete(update_user)
            db.session.commit()
            
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            password = request.form.get("password")
            role = request.form.get("role")

            user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password), role=role)
            db.session.add(user)
            db.session.commit()
            flash("User updated!", category="success")
            return redirect(url_for("views.admin"))

    return render_template("update.html", user = update_user)

@views.route("/<int:id>/delete")
def delete(id):
    delete_user = User.query.filter_by(id = id).first()
    if request.method == "POST":
        if delete_user:
            db.session.delete(delete_user)
            db.session.commit()
            return redirect(url_for("views.admin"))
        abort(404)

    