from datetime import datetime

from flask import (Blueprint, render_template, request, redirect, url_for, flash, abort)
from flask_login import (LoginManager, current_user, login_required, login_user, logout_user)

from .models import db, Patient, Availability, Appointment, AppointmentStatus
from .utils import validate_password, validate_registration

from sqlalchemy.exc import IntegrityError

patients = Blueprint("patients", __name__)

@patients.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("patients.dashboard"))

    if request.method == "POST":
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        errors = validate_registration(username, email, password)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "patient_register.html", username=username, email=email
            )

        # create patient
        patient = Patient(username=username, email=email)
        patient.set_password(password)

        # add it to the table
        db.session.add(patient)
        db.session.commit()

        flash("Your account has been created!!!", "success")
        return redirect(url_for("patients.login"))

    return render_template("patient_register.html")


@patients.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("patients.dashboard"))

    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"]

        patient = Patient.query.filter_by(email=email).first()

        if patient is None or not patient.check_password(password):
            flash("Invalid username or password", "error")
            return render_template("patient_login.html", email=email)

        login_user(patient)
        flash("You are now logged in.", "success")

        return redirect(url_for("patients.dashboard"))

    return render_template("patient_login.html")

@patients.route("/dashboard")
@login_required
def dashboard():
    if not isinstance(current_user, Patient):
        flash("This page is for patients only.", "error")
        return redirect(url_for("main.home"))

    # Fetch patient's upcoming booked appointments

    return render_template("dashboard.html")

@patients.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.home"))


@patients.route("/book")
@login_required
def book():
    if not isinstance(current_user, Patient):
        flash("Only patients can book appointments.", "warning")
        return redirect(url_for("main.home"))

    slots = (
        Availability.query
        .filter(Availability.is_booked == False,
                   Availability.start_time > datetime.now())
        .order_by(Availability.start_time)
        .all()
    )
    return render_template("patients/book.html", slots=slots)

@patients.route("/appointments")
@login_required
def my_appointments():
    appointments = (Appointment.query
                    .filter_by(patient_id=current_user.id)
                    .order_by(Appointment.scheduled_at)
                    .all())
    return render_template("patients/my_appointments.html", appointments=appointments)

@patients.route("/book/<int:availability_id>", methods=["GET", "POST"])
@login_required
def confirm_booking(availability_id):
    if not isinstance(current_user, Patient):
        flash("Only patients can book an appointment", "warning")
        return redirect(url_for("main.home"))

    slot = db.session.get(Availability, availability_id)

    # Slot must exist, still be open, and still be in the future
    if slot is None or slot.is_booked or slot.start_time <= datetime.now():
        flash("That slot is no longer available", "error")
        return redirect(url_for("patients.book"))

    if request.method == "POST":
        reason = request.form.get("reason", "").strip()

        if not reason:
            flash("Please provide a reason for your visit.", "error")
            return render_template("patients/confirm_booking.html", slot=slot)

        appointment = Appointment(
            reason=reason,
            scheduled_at=slot.start_time,
            patient_id=current_user.id,
            availability_id=slot.id
        )

        slot.is_booked = True
        db.session.add(appointment)

        try:
            db.session.commit()
        except IntegrityError:
            # unique = True on availability_id: someone booked this slot first
            db.session.rollback()
            flash("Sorry, that slots was just booked sy someone else", "error")
            return redirect(url_for("patients.book"))

        flash("Your appointment is confirmed!", "success")
        return redirect(url_for("patients.my_appointments"))

    return render_template("patients/confirm_booking.html",slot=slot)


@patients.route('/appointments/<int:appointment_id>/cancel', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.patient_id != current_user.id:
        abort(403)
    if appointment.status != AppointmentStatus.CONFIRMED:
        flash("This appointment can no longer be cancelled.", "warning")
        return redirect(url_for('patients.my_appointments'))

    # free the slot so others can book it
    if appointment.availability:
        appointment.availability.is_booked = False

    appointment.status = AppointmentStatus.CANCELLED
    db.session.commit()
    flash('Appointment cancelled.', 'success')
    return redirect(url_for('patients.my_appointments'))


@patients.route('/appointments/<int:appointment_id>/reschedule', methods=['GET', 'POST'])
@login_required
def reschedule_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if appointment.patient_id != current_user.id:
        abort(403)
    if appointment.status != AppointmentStatus.CONFIRMED:
        flash('This appointment cannot be rescheduled.', 'warning')
        return redirect(url_for('patients.my_appointments'))

    professional = appointment.availability.professional

    open_slots = Availability.query.filter(
        Availability.professional_id == professional.id,
        Availability.is_booked == False,
        Availability.start_time > datetime.now()
    ).order_by(Availability.start_time).all()

    if request.method == 'POST':
        new_slot = Availability.query.get(request.form.get('availability_id'))

        if not new_slot or new_slot.is_booked or new_slot.professional_id != professional.id:
            flash('That slot is no longer available.', 'danger')
            return redirect(url_for('booking.reschedule_appointment',
                                    appointment_id=appointment.id))

        # release old slot, claim new one
        appointment.availability.is_booked = False
        new_slot.is_booked = True
        appointment.availability = new_slot
        appointment.scheduled_at = new_slot.start_time
        db.session.commit()

        flash('Appointment rescheduled.', 'success')
        return redirect(url_for('patients.my_appointments'))

    return render_template('patients/reschedule.html',
                           appointment=appointment,
                           professional=professional,
                           slots=open_slots)