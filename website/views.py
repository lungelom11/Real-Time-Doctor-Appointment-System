from flask import Blueprint, render_template, request,redirect, url_for, flash, session
from .models import User
from . import db
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")



@views.route("/book", methods=["GET","POST"])
@login_required
def book():
    return render_template("book.html", user=current_user)

@views.route("/admin", methods=["GET","POST"])
@login_required
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

@views.route("/delete/<int:id>")
def delete(id):
    delete_user = User.query.get_or_404(id)
    db.session.delete(delete_user)
    db.session.commit()
    flash("User Deleted", category="success")
    return redirect(url_for("views.admin"))

    