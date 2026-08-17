# Validation helper
from datetime import datetime

from sqlalchemy import func

from .models import Patient, Professional


def validate_password(password):
    if len(password) < 8:
        return "Password must contain at least 8 characters."

    if len(password) > 20:
        return "Password must contain at most 20 characters."

    if not any(character.isupper() for character in password):
        return "Password must contain at least an uppercase letter."
    
    if not any(character.isdigit() for character in password):
        return "Password must contain a digit."
    
    return None


def validate_email(email):
    if not email:
        return "Email is required."

    if len(email) > 255:
        return "Email must contain at most 255 characters."

    if "@" not in email:
        return "Invalid email address."

    return None

def validate_credentials(username, email, password,model):
    errors = []

    if not username:
        errors.append("Username is required")
    elif len(username) > 50:
        errors.append("Username may contain at most 50 characters.")
    elif any(character.isspace() for character in username):
        errors.append("Username may not contain whitespace.")
    elif model.query.filter_by(username=username).first():
        errors.append("That username is already in use!")

    email_error = validate_email(email)
    if email_error:
        errors.append(email_error)
    elif model.query.filter_by(email=email).first():
        errors.append("That email is already registered.")

    password_error = validate_password(password)
    if password_error:
        errors.append(password_error)

    return errors

def validate_patient_registration(email, password):
    errors = []

    email_error = validate_email(email)
    if email_error:
        errors.append(email_error)
    elif Patient.query.filter_by(email=email).first():
        errors.append("That email is already registered.")

    password_error = validate_password(password)
    if password_error:
        errors.append(password_error)

    return errors

def validate_professional_registration(username, email, password, firstname, lastname, specialty, bio):
    errors =validate_credentials(username, email, password, Professional)

    if not firstname:
        errors.append("First name is required.")
    elif len(firstname) > 150:
        errors.append("First name may contain at most 150 characters.")

    if not lastname:
        errors.append("Last name is required.")
    elif len(lastname)  > 150:
        errors.append("Lastname may contain at most 150 characters.")

    if not specialty:
        errors.append("Specialty is required.")

    return errors

def validate_slot(date_str, start_str, end_str):
    """ Return (start, end, error). The error is None when the slot is valid."""
    try:
        start = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        return None, None, "Please enter a valid date and times."

    if end <= start:
        return None, None, "End time must be after the start time."

    if start <= datetime.now():
        return None, None, "Availability must be in the future."

    return start, end , None

def validate_phone(phone):
    if not phone:
        return "Phone number is required."

    if len(phone) > 20:
        return "Phone number may contain at most 20 characters."

    digits =[character for character in phone if character.isdigit()]
    if len(digits) < 7:
        return "Please enter a valid phone number."

    return None


def validate_profile(firstname, lastname,email, phone, dob_str, patient):
    """Validate patient profile edits. Returns (errors, dob)."""
    errors = []
    dob = None

    if not firstname:
        errors.append("Firstname is required.")
    elif len(firstname) > 150:
        errors.append("First name may contain at most 150 characters.")

    if not lastname:
        errors.append("Last name is required.")
    elif len(lastname) > 150:
        errors.append("Last name may contain at most 150 characters.")

    email_error = validate_email(email)
    if email_error:
        errors.append(email_error)
    # Exclude the current Patient so saving an unchanged email is allowed
    elif Patient.query.filter(
        Patient.email == email, Patient.id != patient.id
    ).first():
        errors.append("That email is already in use.")

    phone_error = validate_phone(phone)
    if phone_error:
        errors.append(phone_error)

    if not dob_str:
        errors.append("Date of birth is required.")
    else:
        try:
            dob= datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            errors.append("Please enter a valid date of birth.")
        else:
            if dob > datetime.now().date():
                errors.append("Date of birth cannot be in the future.")
    return errors, dob


def find_user_by_email(email):
   """Return the Patient or Professional with this email, or None."""
   email = (email or "").strip().lower()
   if not email:
       return None
   return (
       Patient.query
       .filter(func.lower(Patient.email)==email).first()
       or Professional.query.filter(func.lower(Professional.email) ==email).first()
   )

def dashboard_for(user):
    """Endpoint name of the dashboard belonging to this user type"""
    if isinstance(user, Professional):
        return "professional.dashboard"
    return "patients.dashboard"