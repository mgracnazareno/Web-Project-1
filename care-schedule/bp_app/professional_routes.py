
from datetime import datetime
from bp_app.models import db, Professional, Availability
from .utils import validate_registration, validate_professional_registration
from flask_login import (LoginManager, current_user, login_user, login_required,logout_user)
from flask import Blueprint, flash, render_template, redirect, url_for, request

professional = Blueprint("professional", __name__)


SPECIALTIES = [
    "Family Medicine",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Psychiatry",
    "Physiotherapy",
    "Dentistry",
]

@professional.route("/professional/dashboard")
@login_required
def dashboard():
    return render_template("/professional/dashboard.html")


@professional.route("/professional/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("professional.dashboard"))

    if request.method == "POST":
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        firstname = request.form['firstname'].strip()
        lastname = request.form['lastname'].strip()
        specialty = request.form['specialty'].strip()
        bio = request.form['biography'].strip()

        errors = validate_professional_registration(username, email, password, firstname, lastname, specialty, bio)

        if errors:
            for error in errors:
                flash(error, "danger")
                # re-render the form, keeping what the user typed (except password)
            return render_template(
                    "professional/register.html",
                    username=username,
                    email=email,
                    firstname=firstname,
                    lastname=lastname,
                    specialty=specialty,
                    bio=bio,
                )

            # No errors - create and save the Professional
        professional_user = Professional(
            username=username,
            email=email,
            firstname=firstname,
            lastname=lastname,
            specialty=specialty,
            biography=bio,
        )

        professional_user.set_password(password)

        db.session.add(professional_user)
        db.session.commit()

        flash("Your account has been created!!!", "success")
        return redirect(url_for("professional.login"))

    # GET request
    return render_template("professional/register.html")

@professional.route("/professional/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated and isinstance(current_user, Professional):
        return redirect(url_for("professional.dashboard"))

    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        professional_user = Professional.query.filter_by(email=email).first()

        if professional_user is None:
            flash("No account found with that email. Please register.", "error")
            return redirect(url_for("professional.register"))

        if professional_user is None or not professional_user.check_password(password):
            flash("Invalid email or password", "error")
            return render_template("professional/login.html",  email=email)

        login_user(professional_user)

        flash("You are now logged in.", "success")
        return redirect(url_for("professional.dashboard"))

    return render_template("professional/login.html")



@professional.route("/professional/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.home"))

@professional.route("/professional/availability/add", methods=["GET", "POST"])
@login_required
def add_availability():
    if not isinstance(current_user, Professional):
        flash("This page is for Professionals only.", "danger")
        return redirect(url_for("main.home"))

    if request.method == "POST":
        date_str = request.form.get("date", "")
        start_str = request.form.get("start_time", "")
        end_str = request.form.get("end_time", "")

        # datetime - local inputs
        try:
            start = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
            end = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            flash("Please enter a valid date and times.", "danger")
            return render_template("professional/add_availability.html")

        if end <= start:
            flash("End tiime must be after the start time.", "error")
            return render_template("professional/add_availability.html")

        if start <= datetime.now():
            flash("Availability must be in the future.", "error")
            return render_template("professional/add_availability.html")

        overlap = Availability.query.filter(
            Availability.professional_id == current_user.id,
            Availability.start_time < end,
            Availability.end_time > start
        ).first()

        if overlap:
            flash("This time overlaps one of your existing slots", "error")
            return render_template("professional/add_availability.html")

        slot = Availability(
            professional_id=current_user.id,
            start_time=start,
            end_time=end,
        )
        db.session.add(slot)
        db.session.commit()

        flash("Availability added", "success")
        return redirect(url_for("/professional.add.availability"))

    return render_template("professional/add_availability.html")

