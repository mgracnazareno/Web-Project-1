from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/user-login")
def get_started():
    # kung naka-login na, huwag na ipakita ang role picker
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    # "register" o "login" — para reusable ang isang page
    action = request.args.get("action", "register")
    return render_template("user-login.html", action=action)



