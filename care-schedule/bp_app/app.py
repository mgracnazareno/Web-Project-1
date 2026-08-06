from datetime import datetime
import os
from dotenv import load_dotenv

from flask import (Flask, jsonify, render_template, request)
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy

# loads environment variables from .env file First
load_dotenv()

from .models import db, Patient
from .main_routes import main
from .patient_routes import patients

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///appointments.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "dev-fallback-key-change-in-prod"
)

# db = SQLAlchemy(app)
# initialize extensions
db.init_app(app)

# login
login_manager = LoginManager()
login_manager.login_view = "patients.login"
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(main)
app.register_blueprint(patients)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Patient, int(user_id))