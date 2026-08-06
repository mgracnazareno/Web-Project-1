import os
from dotenv import load_dotenv

from datetime import datetime
from flask import (Flask, jsonify, render_template, request)
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)

from .models import db

from .main_routes import main

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///appointments.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db = SQLAlchemy(app)

db.init_app(app)

# login
login_manager = LoginManager()
login_manager.login_view = "login"

login_manager.init_app(app)

app.register_blueprint(main)

with app.app_context():
    db.create_all()