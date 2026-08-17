from urllib.parse import urlparse
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from .utils import find_user_by_email, dashboard_for

auth = Blueprint("auth", __name__)

def is_safe_url(target):
    """Only allow redirects that stay on the site."""
    return target and urlparse(target).netloc == ""

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(dashboard_for(current_user)))

    if request.method == "POST":
        email = request.form.get("email", "")
        password =  request.form.get("password", "")

        user = find_user_by_email(email)
        if user is None or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html", email=email), 401

        login_user(user)

        next_page = request.args.get("next")
        if is_safe_url(next_page):
            return redirect(next_page)
        return redirect(url_for(dashboard_for(user)))
    return render_template("auth/login.html")

@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.home"))
