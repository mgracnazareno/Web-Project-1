
import os
from dotenv import load_dotenv

from bp_app.models import db, Professional
from utils import validate_registration, validate_professional_registration
from flask_login import current_user
from flask import Blueprint, flash, render_template, redirect, url_for, request

professional = Blueprint("professional", __name__)

@professional.route("/professional/dashboard")
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
                # re-render the form, keepint what the user typed (except password)
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