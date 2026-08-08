import enum
from flask_login import UserMixin

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import (check_password_hash, generate_password_hash)

db = SQLAlchemy()
class Patient(UserMixin, db.Model):
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key = True)

    email = db.Column(db.String(255), nullable = False, unique=True)

    username = db.Column(db.String(100), nullable = False, unique= True)

    password_hash = db.Column(db.String(255), nullable = False)

    firstname = db.Column(db.String(150), nullable = True)

    lastname = db.Column(db.String(150), nullable = True)

    phone = db.Column(db.String(15), nullable = True)

    dob = db.Column(db.Date)

    appointments = db.relationship("Appointment", back_populates="patient")

    # methods
    # Flask-login can tell a Patient apart from a Professional with the same numeric id
    def get_id(self):
        return f"Patient:{self.id}"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Patient{self.id}: {self.username}>"

class AppointmentStatus(enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


class Appointment(db.Model):
    __tablename__ = "appointment"

    id = db.Column(db.Integer, primary_key = True)

    reason = db.Column(db.Text, nullable = False)

    status = db.Column(db.Enum(AppointmentStatus), nullable= False, default = AppointmentStatus.CONFIRMED)

    scheduled_at = db.Column(db.DateTime, nullable=False)

    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable = False)

    patient = db.relationship("Patient", back_populates="appointments")

    availability_id = db.Column(
        db.Integer,
        db.ForeignKey("availability.id"),
        nullable=False,
        unique=True  # one slot can be booked once
    )

    availability = db.relationship(
        "Availability",
        back_populates="appointment"
    )


class Professional(UserMixin, db.Model):
    __tablename__ = "professional"

    id = db.Column(db.Integer, primary_key = True)

    email = db.Column(db.String(255), nullable = False, unique = True)

    username = db.Column(db.String(255), nullable = False, unique= True)

    password_hash = db.Column(db.String(255), nullable = False)

    firstname = db.Column(db.String(150), nullable = True)

    lastname = db.Column(db.String(150), nullable = True)

    specialty = db.Column(db.String(150), nullable = True)

    biography = db.Column(db.Text)

    availabilities = db.relationship(
        "Availability",
        back_populates = "professional"
    )

    def get_id(self):
        return f"Professional:{self.id}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Availability(db.Model):
    __tablename__ = "availability"

    id = db.Column(db.Integer, primary_key = True)

    start_time = db.Column(db.DateTime, nullable = False)

    end_time = db.Column(db.DateTime, nullable = False)

    is_booked = db.Column(db.Boolean, nullable = False, default = False)

    professional_id = db.Column(
        db.Integer,
        db.ForeignKey("professional.id"),
        nullable = False
    )

    professional = db.relationship(
        "Professional",
        back_populates = "availabilities"
    )

    # One slot has at most one appointment
    appointment = db.relationship("Appointment", back_populates="availability", uselist=False)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.start_time.date().isoformat(),         # "2026-08-05"
            "start_time": self.start_time.strftime("%H:%M"),    # "14:30"
            "end_time": self.end_time.strftime("%H:%M"),
            "is_booked": self.is_booked,
            "professional_id": self.professional_id
        }
