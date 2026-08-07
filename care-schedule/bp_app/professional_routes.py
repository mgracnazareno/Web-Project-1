from flask import Blueprint, render_template

professional = Blueprint("professional", __name__)

@professional.route("/professional/dashboard")
def dashboard():
    return render_template("dashboard.html")


