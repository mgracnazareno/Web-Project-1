# Validation helper
from datetime import datetime
from .models import Patient, Professional


def validate_password(password):
    if len(password) < 8:
        return "Password must contain at least  8 characters."

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

def validate_registration(email, password):
    errors = []

    if not email:
        errors.append("Email is required.")
    elif Patient.query.filter_by(email=email).first():
        errors.append("That email is already registered.")

    # Password validation
    password_error = validate_password(password)
    if password_error:
        errors.append(password_error)

    return errors

def validate_credentials(username, email, password,model):
    errors = []

    if not username:
        errors.append("Username is required")
    elif len(username) > 50:
        errors.append("Username may contain at most 50 characters.")
    elif any(character.isspace() for character in username):
        errors.append("Username may not contain whitespace.")

    if model.query.filter_by(username=username).first():
        errors.append("That username is already in use!")

    if model.query.filter_by(email=email).first():
        errors.append("That email is already registered.")

    email_error = validate_email(email)
    if email_error:
        errors.append(email_error)

    password_error = validate_password(password)
    if password_error:
        errors.append(password_error)

    return errors

def validate_patient_registration(username, email, password):
    return validate_credentials(username, email, password, Patient)

def validate_professional_registration(username, email, password, firstname, lastname, specialty, bio):
    errors =validate_credentials(username, email, password, Professional)

    if not firstname:
        errors.append("First name is required.")
    elif len(firstname) > 50:
        errors.append("First name may contain at most 50 characters.")
    elif any(character.isspace() for character in firstname):
        errors.append("First name may not contain whitespace.")
    return errors

def validate_slot(date_str, start_str, end_str):
    """ Return (start, end, error). The error is None when the slot is valid."""
    try:
        start = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{date_str}{end_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        return None, None, "Please enter a valid date and times."

    if end <= start:
        return None, None, "End time must be after the start time."

    if start <= datetime.now():
        return None, None, "Availability must be in the future."

    return start, end , None

