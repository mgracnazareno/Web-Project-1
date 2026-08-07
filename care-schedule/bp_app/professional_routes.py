
import os
from dotenv import load_dotenv
from utils import validate_registration
from flask_login import current_user
from flask import Blueprint, render_template, redirect, url_for, request

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

        errors = validate_registration(username, email, password)
    return None