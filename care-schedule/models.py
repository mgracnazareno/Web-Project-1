import enum
from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import (check_password_hash, generate_password_hash)

db = SQLAlchemy()
class Patient(UserMixin, db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key = True)

    email = db.Column(db.String(255), nullable = False)

    username = db.Column(db.String(100), nullable = False)

    password_hash = db.Column(db.String(255), nullable = False)

    firstname = db.Column(db.String(150), nullable = False)

    lastname = db.Column(db.String(150), nullable = False)

    phone = db.Column(db.String(15), nullable = False)

    dob = db.Column(db.Date)

    appointments = db.relationship("Appointment", back_populates="patient")

    # methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return(f"<Patient {self.id}: {self.username}>")


class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key = True)

    reason = db.Column(db.Text, nullable = False)

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable = False)

    patient = db.relationship("Patient", back_populates="appointments")

