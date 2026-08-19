from datetime import datetime, date, timedelta
from flask import (Blueprint, render_template, request, redirect, url_for, flash, abort)
from flask_login import (current_user, login_required, login_user, logout_user)

from .models import db, Patient, Availability, Appointment, AppointmentStatus, Professional
from .utils import validate_patient_registration, validate_profile

from sqlalchemy.exc import IntegrityError

patients = Blueprint("patients", __name__)


@patients.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("patients.dashboard"))

    if request.method == "POST":
        firstname = request.form.get("firstname", "").strip()
        lastname = request.form.get("lastname", "").strip()
        email = request.form.get('email', "").strip()
        password = request.form.get("password", "")
        dob_str = request.form.get("dob", "").strip()
        phone = request.form.get("phone", "").strip()

        errors = validate_patient_registration(email, password)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "patient_register.html", email=email
            )

        dob = None
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            errors.append("Please enter a valid date of birth.")

        # create patient
        patient = Patient(
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            dob=dob,
        )
        patient.set_password(password)

        # add it to the table
        db.session.add(patient)
        db.session.commit()

        flash("Your account has been created!!!", "success")
        return redirect(url_for("auth.login"))

    return render_template("patient_register.html")


# @patients.route("/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for("patients.dashboard"))
#
#     if request.method == "POST":
#         email = request.form["email"].strip()
#         password = request.form["password"]
#
#         patient = Patient.query.filter_by(email=email).first()
#
#         if patient is None or not patient.check_password(password):
#             flash("Invalid email or password", "error")
#             return render_template("patient_login.html", email=email)
#
#         login_user(patient)
#         flash("You are now logged in.", "success")
#
#         return redirect(url_for("patients.dashboard"))
#
#     return render_template("patient_login.html")

@patients.route("/dashboard")
@login_required
def dashboard():
    if not isinstance(current_user, Patient):
        flash("This page is for patients only.", "error")
        return redirect(url_for("main.home"))

    # Fetch patient's upcoming booked
    now = datetime.now()

    appointments = (
        Appointment.query
        .filter_by(patient_id=current_user.id)
        .order_by(Appointment.scheduled_at)
        .all()
    )

    upcoming = [apt for apt in appointments
                if apt.status == AppointmentStatus.CONFIRMED and apt.scheduled_at > now]
    completed = [apt for apt in appointments if apt.status == AppointmentStatus.COMPLETED]
    cancelled = [apt for apt in appointments if apt.status == AppointmentStatus.CANCELLED]

    # Split upcoming into the hearo card and the list below it
    next_appointment = upcoming[0] if upcoming else None
    later_appointments = upcoming[1:]

    # Seven days starting today, for the strip on the right
    week = [date.today() + timedelta(days=offset) for offset in range(7)]
    booked_days = {a.scheduled_at.date() for a in upcoming}

    if now.hour < 12:
        greeting = "Good morning"
    elif now.hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return render_template(
        "patients/dashboard.html",
        upcoming=upcoming,
        completed=completed,
        cancelled=cancelled,
        next_appointment=next_appointment,
        later_appointments=later_appointments,
        week=week,
        booked_days=booked_days,
        greeting=greeting,
        active_page="dashboard",

    )


@patients.route("/logout", methods=["POST"])
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

    # Read the search filters from the URL
    query = request.args.get("query", "").strip()
    selected_specialty = request.args.get("specialty", "").strip()
    available_only = request.args.get("available")=="1"

    now = datetime.now()


    # How many open slots each professional has
    open_slots = (
        Availability.query
        .filter(Availability.is_booked == False,
                Availability.start_time > datetime.now())
        .order_by(Availability.start_time)
        .all()
    )

    # How many open slots each professional has,
    slot_counts = {}
    for slot in open_slots:
        slot_counts[slot.professional_id] = slot_counts.get(slot.professional_id, 0) + 1

    # Build the professional list, narrowing it by whatever filters were given
    professional_query = Professional.query

    if query:
        like = f"%{query}%"
        professional_query = professional_query.filter(
            db.or_(
                Professional.firstname.ilike(like),
                Professional.lastname.ilike(like),
                Professional.specialty.ilike(like),
            )
        )
    if selected_specialty:
        professional_query = professional_query.filter(
            Professional.specialty == selected_specialty
        )
    professionals = professional_query.order_by(Professional.lastname).all()

    if available_only:
        professionals = [p for p in professionals if slot_counts.get(p.id, 0) > 0]

    # Every specialty currently in use, for the dropdown
    specialties = [
        row[0] for row in
        db.session.query(Professional.specialty).distinct()
        .order_by(Professional.specialty).all()
        if row[0]
    ]
    selected_id = request.args.get("professional_id", type=int)
    selected = db.session.get(Professional, selected_id) if selected_id else None

    slots = [slot for slot in open_slots if selected and slot.professional_id == selected_id]
    return render_template(
        "patients/book.html",
        professionals=professionals,
        slot_counts=slot_counts,
        selected=selected,
        slots=slots,
        query=query,
        selected_specialty=selected_specialty,
        available_only=available_only,
        specialties=specialties,
        active_page="book",
    )


@patients.route("/appointments")
@login_required
def my_appointments():
    appointments = (Appointment.query
                    .filter(Appointment.patient_id==current_user.id,
                            Appointment.status == AppointmentStatus.CONFIRMED,
                            Appointment.scheduled_at > datetime.now())
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

    return render_template("patients/confirm_booking.html", slot=slot)


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


@patients.route("/history")
@login_required
def history():
    if not isinstance(current_user, Patient):
        abort(403)

    past = (
        Appointment.query
        .filter(Appointment.patient_id == current_user.id)
        .filter(Appointment.status != AppointmentStatus.CONFIRMED)
        .order_by(Appointment.scheduled_at.desc())
        .all()
    )
    return render_template("patients/history.html", past=past, active_page="history")


@patients.route("/patients/profile", methods=["GET", "POST"])
@login_required
def profile():
    if not isinstance(current_user, Patient):
        abort(403)

    form = {
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
        "email": current_user.email,
        "phone": current_user.phone,
        "dob": current_user.dob.isoformat(),
    }

    if request.method == "POST":
        # Keep what the user typed so a failed save doesn't wipe the form
        form = {key: request.form.get(key, "").strip() for key in form}
        form["email"] = form["email"].lower()

        errors, dob = validate_profile(
            form["firstname"], form["lastname"], form["email"],
            form["phone"], form["dob"], current_user,
        )

        if errors:
            for message in errors:
                flash(message, "danger")
            return render_template(
                "patients/profile.html",
                form=form,
                today=datetime.now().date().isoformat(),
                active_page="profile"
            ), 400

        current_user.firstname = form["firstname"]
        current_user.lastname = form["lastname"]
        current_user.email = form["email"]
        current_user.phone = form["phone"]
        current_user.dob = dob
        db.session.commit()

        flash("Your profile has been updated.", "success")
        return redirect(url_for("patients.profile"))

    return render_template(
        "patients/profile.html",
        form=form,
        today=datetime.now().date().isoformat(),
        active_page="profile",
    )
