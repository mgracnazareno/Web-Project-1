from flask import (Blueprint, render_template, request, redirect, url_for, flash)
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)

from .models import db, Patient
from .utils import validate_password

patients = Blueprint("patients", __name__, url_prefix="/patient")

@patients.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("patients.dashboard"))

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        patient = Patient.query.filter_by(username=username).first()

        if patient is None or not patient.check_password(password):
            flash("Invalid username or password", "error")
            return render_template("patient_login.html", username=username)

        login_user(patient)
        flash("You are not logged in.", "success")

        return redirect(url_for("dashboard"))

    return render_template("patient_login.html")


