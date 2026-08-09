from datetime import datetime

from flask import (Blueprint, render_template, request, redirect, url_for, flash)
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)

from .models import db, Patient, Availability, Appointment
from .utils import validate_password, validate_registration

from sqlalchemy.exc import IntegrityError

patients = Blueprint("patients", __name__)

@patients.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("patients.dashboard"))

    if request.method == "POST":
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        errors = validate_registration(username, email, password)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "patient_register.html", username=username, email=email
            )

        # create patient
        patient = Patient(username=username, email=email)
        patient.set_password(password)

        # add it to the table
        db.session.add(patient)
        db.session.commit()

        flash("Your account has been created!!!", "success")
        return redirect(url_for("patients.login"))

    return render_template("patient_register.html")


@patients.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("patients.dashboard"))

    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        patient = Patient.query.filter_by(email=email).first()

        if patient is None or not patient.check_password(password):
            flash("Invalid username or password", "error")
            return render_template("patient_login.html", email=email)

        login_user(patient)
        flash("You are now logged in.", "success")

        return redirect(url_for("patients.dashboard"))

    return render_template("patient_login.html")

@patients.route("/dashboard")
@login_required
def dashboard():
    if not isinstance(current_user, Patient):
        flash("This page is for patients only.", "error")
        return redirect(url_for("main.home"))

    # Fetch patient's upcoming booked appointments

    return render_template("dashboard.html")

@patients.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.home"))


@patients.route("/book")
@login_required
def book():
    if not isinstance(current_user, Patient):
        flash("Only patients can book appointments.", "warning")
        return redirect(url_for("main.home"))

    slots = (
        Availability.query
        .filter(Availability.is_booked == False,
                   Availability.start_time > datetime.now())
        .order_by(Availability.start_time)
        .all()
    )
    return render_template("patients/book.html", slots=slots)

@patients.route("/appointments")
@login_required
def my_appointments():
    appointments = (Appointment.query
                    .filter_by(patient_id=current_user.id)
                    .order_by(Appointment.scheduled_at)
                    .all())
    return render_template("patients/my_appointments.html", appointments=appointments)