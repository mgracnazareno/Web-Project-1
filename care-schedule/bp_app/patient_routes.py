from datetime import datetime, date, timedelta
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from .models import db, Patient, Availability, Appointment, AppointmentStatus, Professional
from .utils import (
    validate_patient_registration,
    validate_profile,
    parse_dob,
    format_week_label,
    greeting_for_time,
    validate_booking_reason,
    is_slot_bookable,
)

patients = Blueprint("patients", __name__)

def conflicting_appointment(patient_id, slot, exclude_id=None):
    """Return the patient's confirmed appointment overlapping this slot, if any."""
    query = (
        Appointment.query
        .join(Availability, Appointment.availability_id == Availability.id)
        .filter(
            Appointment.patient_id == patient_id,
            Appointment.status == AppointmentStatus.CONFIRMED,
            Availability.start_time < slot.end_time,
            Availability.end_time > slot.start_time,
        )
    )

    if exclude_id is not None:
        query = query.filter(Appointment.id != exclude_id)
    return query.first()


def patient_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not isinstance(current_user, Patient):
            flash("This page is for patients only.", "error")
            return redirect(url_for("main.home"))
        return f(*args, **kwargs)
    return decorated


@patients.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("patients.dashboard"))

    if request.method == "POST":
        firstname = request.form.get("firstname", "").strip()
        lastname = request.form.get("lastname", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        dob_str = request.form.get("dob", "").strip()
        phone = request.form.get("phone", "").strip()

        errors = validate_patient_registration(email, password)

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("patients/patient_register.html", email=email)

        dob, dob_error = parse_dob(dob_str)
        if dob_error:
            errors.append(dob_error)

        patient = Patient(
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            dob=dob,
        )
        patient.set_password(password)

        db.session.add(patient)
        db.session.commit()

        flash("Your account has been created!", "success")
        return redirect(url_for("auth.login"))

    return render_template("patients/patient_register.html")


@patients.route("/dashboard")
@login_required
@patient_required
def dashboard():
    now = datetime.now()

    appointments = (
        Appointment.query
        .filter_by(patient_id=current_user.id)
        .order_by(Appointment.scheduled_at)
        .all()
    )

    upcoming = [a for a in appointments
                if a.status == AppointmentStatus.CONFIRMED and a.scheduled_at > now]
    completed = [a for a in appointments if a.status == AppointmentStatus.COMPLETED]
    cancelled = [a for a in appointments if a.status == AppointmentStatus.CANCELLED]

    next_appointment = upcoming[0] if upcoming else None
    later_appointments = upcoming[1:]

    week = [date.today() + timedelta(days=i) for i in range(7)]
    booked_days = {a.scheduled_at.date() for a in upcoming}

    week_label = format_week_label(week)
    greeting = greeting_for_time(now)

    return render_template(
        "patients/dashboard.html",
        upcoming=upcoming,
        completed=completed,
        cancelled=cancelled,
        next_appointment=next_appointment,
        later_appointments=later_appointments,
        week=week,
        week_label=week_label,
        today=date.today(),
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
@patient_required
def book():
    query = request.args.get("query", "").strip()
    selected_specialty = request.args.get("specialty", "").strip()
    available_only = request.args.get("available") == "1"

    now = datetime.now()

    open_slots = (
        Availability.query
        .filter(Availability.is_booked == False, Availability.start_time > now)
        .order_by(Availability.start_time)
        .all()
    )

    slot_counts = {}
    for slot in open_slots:
        slot_counts[slot.professional_id] = slot_counts.get(slot.professional_id, 0) + 1

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

    specialties = [
        row[0] for row in
        db.session.query(Professional.specialty).distinct().order_by(Professional.specialty).all()
        if row[0]
    ]

    selected_id = request.args.get("professional_id", type=int)
    selected = db.session.get(Professional, selected_id) if selected_id else None
    slots = [s for s in open_slots if selected and s.professional_id == selected_id]

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
@patient_required
def my_appointments():
    appointments = (
        Appointment.query
        .filter(
            Appointment.patient_id == current_user.id,
            Appointment.status == AppointmentStatus.CONFIRMED,
            Appointment.scheduled_at > datetime.now(),
        )
        .order_by(Appointment.scheduled_at)
        .all()
    )
    return render_template("patients/my_appointments.html", appointments=appointments)


@patients.route("/book/<int:availability_id>", methods=["GET", "POST"])
@login_required
@patient_required
def confirm_booking(availability_id):
    slot = db.session.get(Availability, availability_id)

    if not is_slot_bookable(slot):
        flash("That slot is no longer available.", "error")
        return redirect(url_for("patients.book"))

    conflict = conflicting_appointment(current_user.id, slot)
    if conflict:
        flash(
            f"You already have an appointment with Dr. {conflict.professional.lastname} "
            f"at that time. Cancel or reschedule it first.",
            "error",
        )
        return redirect(url_for("patients.book", professional_id=slot.professional_id))

    if request.method == "POST":
        reason = request.form.get("reason", "").strip()

        reason_error = validate_booking_reason(reason)
        if reason_error:
            flash(reason_error, "error")
            return render_template("patients/confirm_booking.html", slot=slot)

        reserved = db.session.execute(
            db.update(Availability)
            .where(Availability.id == slot.id, Availability.is_booked == False)
            .values(is_booked=True)
        ).rowcount

        if not reserved:
            db.session.rollback()
            flash("Sorry, that slot was just booked by someone else.", "error")
            return redirect(url_for("patients.book"))

        appointment = Appointment(
            reason=reason,
            scheduled_at=slot.start_time,
            patient_id=current_user.id,
            availability_id=slot.id,
            professional_id=slot.professional_id,
        )
        db.session.add(appointment)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Sorry, that slot was just booked by someone else.", "error")
            return redirect(url_for("patients.book"))

        flash("Your appointment is confirmed!", "success")
        return redirect(url_for("patients.my_appointments"))

    return render_template("patients/confirm_booking.html", slot=slot)


@patients.route("/appointments/<int:appointment_id>/cancel", methods=["POST"])
@login_required
@patient_required
def cancel_appointment(appointment_id):
    appointment = db.get_or_404(Appointment, appointment_id)

    if appointment.patient_id != current_user.id:
        abort(403)
    if appointment.status != AppointmentStatus.CONFIRMED:
        flash("This appointment can no longer be cancelled.", "warning")
        return redirect(url_for("patients.my_appointments"))

    slot = appointment.availability
    if slot:
        slot.is_booked = False
        appointment.availability = None

    appointment.status = AppointmentStatus.CANCELLED
    db.session.commit()
    flash("Appointment cancelled.", "success")
    return redirect(url_for("patients.my_appointments"))


@patients.route("/appointments/<int:appointment_id>/reschedule", methods=["GET", "POST"])
@login_required
@patient_required
def reschedule_appointment(appointment_id):
    appointment = db.get_or_404(Appointment, appointment_id)

    if appointment.patient_id != current_user.id:
        abort(403)
    if appointment.status != AppointmentStatus.CONFIRMED:
        flash("This appointment cannot be rescheduled.", "warning")
        return redirect(url_for("patients.my_appointments"))

    professional = appointment.professional

    open_slots = (
        Availability.query
        .filter(
            Availability.professional_id == professional.id,
            Availability.is_booked == False,
            Availability.start_time > datetime.now(),
        )
        .order_by(Availability.start_time)
        .all()
    )

    if request.method == "POST":
        new_slot_id = request.form.get("availability_id", type=int)
        new_slot = db.session.get(Availability, new_slot_id)

        if not is_slot_bookable(new_slot, professional_id=professional.id):
            flash("That slot is no longer available.", "warning")
            return redirect(url_for("patients.reschedule_appointment", appointment_id=appointment.id))

        conflict = conflicting_appointment(current_user.id, new_slot, exclude_id=appointment.id)
        if conflict:
            flash(
                f"That time overlaps your appointment with Dr. {conflict.professional.lastname}.",
                "error",
            )
            return redirect(url_for("patients.reschedule_appointment", appointment_id=appointment.id))

        appointment.availability.is_booked = False
        new_slot.is_booked = True
        appointment.availability = new_slot
        appointment.professional_id = new_slot.professional_id
        appointment.scheduled_at = new_slot.start_time
        db.session.commit()

        flash("Appointment rescheduled.", "success")
        return redirect(url_for("patients.my_appointments"))

    return render_template(
        "patients/reschedule.html",
        appointment=appointment,
        professional=professional,
        slots=open_slots,
    )


@patients.route("/history")
@login_required
@patient_required
def history():
    past = (
        Appointment.query
        .filter(
            Appointment.patient_id == current_user.id,
            Appointment.status != AppointmentStatus.CONFIRMED,
        )
        .order_by(Appointment.scheduled_at.desc())
        .all()
    )
    return render_template("patients/history.html", past=past, active_page="history")


@patients.route("/patients/profile", methods=["GET", "POST"])
@login_required
@patient_required
def profile():
    form = {
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
        "email": current_user.email,
        "phone": current_user.phone,
        "dob": current_user.dob.isoformat(),
    }

    if request.method == "POST":
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
                active_page="profile",
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