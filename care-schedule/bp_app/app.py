
import os
from dotenv import load_dotenv

from flask import Flask
from flask_login import LoginManager

from .models import db, Patient, Professional
from .main_routes import main
from .patient_routes import patients
from .professional_routes import professional
from .auth_routes import auth

# loads environment variables from .env file First1
load_dotenv()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please sign in to continue."


@login_manager.user_loader
def load_user(user_id):
    try:
        user_type, record_id = user_id.split(":", 1)
        model = {"Patient": Patient, "Professional": Professional}.get(user_type)
        return db.session.get(model, int(record_id)) if model else None
    except (AttributeError, TypeError, ValueError):
        return None


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///careschedule.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY", "dev-fallback-key-change-in-prod"
    )

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(patients)
    app.register_blueprint(professional)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    return app