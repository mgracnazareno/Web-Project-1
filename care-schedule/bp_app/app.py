from datetime import datetime
from flask import (Flask, jsonify, render_template, request)

from .models import db

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///appointments.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

db.init_app(app)

with app.app_context():
    db.create_all()