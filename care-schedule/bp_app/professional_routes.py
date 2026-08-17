from datetime import datetime
from bp_app.models import db, Professional, Availability, Appointment, AppointmentStatus
from .utils import validate_professional_registration
from flask_login import (current_user, login_user, login_required, logout_user)
from flask import Blueprint, flash, render_template, redirect, url_for, request

professional = Blueprint("professional", __name__)

SPECIALTIES = [
    "Family Medicine",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Psychiatry",
    "Physiotherapy",
    "Dentistry",
]


@professional.route("/professional/dashboard")
@login_required
def dashboard():
    if not isinstance(current_user, Professional):
        flash("This page is for professionals only.", "error")
        return redirect(url_for("main.home"))

    now = datetime.now()

    slots = (
        Availability.query
        .filter_by(professional_id=current_user.id)
        .order_by(Availability.start_time.asc())
        .all()
    )

    open_slots = [
        slot for slot in slots
        if slot.start_time >= now and not slot.appointment
    ]

    bookings = (
        Appointment.query
        .join(Availability, Appointment.availability_id == Availability.id)
        .filter(Availability.professional_id == current_user.id)
        .order_by(Availability.start_time.asc())
        .all()
    )

    confirmed = [b for b in bookings if b.status.value == "confirmed"]

    today = [b for b in confirmed if b.availability.start_time.date() == now.date()]
    upcoming = [b for b in confirmed if b.availability.start_time >= now]

    if now.hour < 12:
        greeting = "Good morning"
    elif now.hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return render_template("professional/dashboard.html",
                           active_page="dashboard",
                           greeting=greeting,
                           today_label=now.strftime("%A, %b %d"),
                           today=today,
                           upcoming=upcoming,
                           open_slots=open_slots,
                           slots=slots)



@professional.route("/professional/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("professional.dashboard"))

    if request.method == "POST":
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        firstname = request.form['firstname'].strip()
        lastname = request.form['lastname'].strip()
        specialty = request.form['specialty'].strip()
        bio = request.form['biography'].strip()

        errors = validate_professional_registration(username, email, password, firstname, lastname, specialty, bio)

        if errors:
            for error in errors:
                flash(error, "danger")
                # re-render the form, keeping what the user typed (except password)
            return render_template(
                "professional/register.html",
                specialties=SPECIALTIES,
                username=username,
                email=email,
                firstname=firstname,
                lastname=lastname,
                specialty=specialty,
                biography=bio,
            )

            # No errors - create and save the Professional
        professional_user = Professional(

            username=username,
            email=email,
            firstname=firstname,
            lastname=lastname,
            specialty=specialty,
            biography=bio
        )

        professional_user.set_password(password)

        db.session.add(professional_user)
        db.session.commit()

        flash("Your account has been created!!!", "success")
        return redirect(url_for("auth.login"))

    # GET request
    return render_template("professional/register.html", specialties=SPECIALTIES)


# @professional.route("/professional/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated and isinstance(current_user, Professional):
#         return redirect(url_for("professional.dashboard"))
#
#     if request.method == "POST":
#         email = request.form["email"].strip()
#         password = request.form["password"]
#
#         professional_user = Professional.query.filter_by(email=email).first()
#
#         if professional_user is None:
#             flash("No account found with that email. Please register.", "error")
#             return redirect(url_for("professional.register"))
#
#         if professional_user is None or not professional_user.check_password(password):
#             flash("Invalid email or password", "error")
#             return render_template("professional/login.html", email=email)
#
#         login_user(professional_user)
#
#         flash("You are now logged in.", "success")
#         return redirect(url_for("professional.dashboard"))
#
#     return render_template("professional/login.html")


@professional.route("/professional/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.home"))


@professional.route("/professional/availability/add", methods=["POST"])
@login_required
def add_availability():
    if not isinstance(current_user, Professional):
        flash("This page is for Professionals only.", "danger")
        return redirect(url_for("main.home"))

    date_str = request.form.get("date", "")
    start_times = request.form.getlist("start_time")
    end_str = request.form.getlist("end_time")

    if not date_str or not start_times:
        flash("Please pick a data and at least one time range.", "error")
        return redirect(url_for("professional.manage_availability"))

    # Slots added
    added = 0

    for start_str, end_str in zip(start_times, end_str):
        if not start_str or not end_str:
            continue

        # datetime - local inputs
        try:
            start = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
            end = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            flash(f"{start_str}Please enter a valid date and times.", "danger")
            continue

        if end <= start:
            flash(f"{start_str}End time must be after the start time.", "error")
            continue

        if start <= datetime.now():
            flash("Availability must be in the future.", "error")
            continue

        overlap = Availability.query.filter(
            Availability.professional_id == current_user.id,
            Availability.start_time < end,
            Availability.end_time > start
        ).first()

        if overlap:
            flash("This time overlaps one of your existing slots", "error")
            continue

        slot = Availability(
            professional_id=current_user.id,
            start_time=start,
            end_time=end,
        )
        db.session.add(slot)
        added += 1

    if added:
        db.session.commit()
        flash(f"Added {added} slots(s).", "success")
    return redirect(url_for("professional.manage_availability"))


@professional.route("/professional/availability")
@login_required
def manage_availability():
    if not isinstance(current_user, Professional):
        flash("This page is for professionals only.", "error")
        return redirect(url_for('main.home'))

    slots = (
        Availability.query
        .filter_by(professional_id=current_user.id)
        .order_by(Availability.start_time)
        .all()
    )
    return render_template("professional/manage_availability.html", slots=slots)


@professional.route("/professional/availability/<int:slot_id>/edit", methods=["POST"])
@login_required
def edit_availability(slot_id):
    if not isinstance(current_user, Professional):
        flash("This page is for professionals only.", "error")
        return redirect(url_for("main.home"))

    slot = db.session.get(Availability, slot_id)

    if slot is None or slot.professional_id != current_user.id:
        flash("Availability not found", "error")
        return redirect(url_for("professional.manage_availability"))

    if slot.appointment is not None:
        flash("This slot is booked and can't be edited.", "error")
        return redirect(url_for("professional.manage_availability"))

    date_str = request.form.get("date", "").strip()
    start_str = request.form.get("start_time", "").strip()
    end_str = request.form.get("end_time", "").strip()

    try:
        start_dt = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
        end_dt = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        flash("Please provide a valid date, start time, and end time.", "error")
        return redirect(url_for("professional.manage_availability"))

    if end_dt <= start_dt:
        flash("End time must be after the start time.", "error")
        return redirect(url_for("professional.manage_availability"))

    if start_dt < datetime.now():
        flash("Availability can't be set in the past.", "error")
        return redirect(url_for("professional.manage_availability"))

    overlap = Availability.query.filter(
        Availability.professional_id == current_user.id,
        Availability.id != slot.id,
        Availability.start_time < end_dt,
        Availability.end_time > start_dt,
    ).first()

    if overlap is not None:
        flash("This time overlaps with another one of your slots.", "error")
        return redirect(url_for("professional.manage_availability"))

    slot.start_time = start_dt
    slot.end_time = end_dt
    db.session.commit()
    flash("Availability updated.", "success")
    return redirect(url_for("professional.manage_availability"))


@professional.route("/professional/availability/<int:slot_id>/delete", methods=["POST"])
@login_required
def delete_availability(slot_id):
    if not isinstance(current_user, Professional):
        flash("This page is for professionals only.", "error")
        return redirect(url_for("main.home"))

    slot = db.session.get(Availability, slot_id)

    if slot is None or slot.professional_id != current_user.id:
        flash("Availability not found.", "error")
        return redirect(url_for("professional.manage_availability"))

    if slot.appointment is not None:
        flash("This slot is booked and can't be deleted.", "error")
        return redirect(url_for("professional.manage_availability"))

    db.session.delete(slot)
    db.session.commit()
    flash("Availability removed.", "success")
    return redirect(url_for("professional.manage_availability"))


@professional.route("/professional/appointments")
@login_required
def appointment():
    if not isinstance(current_user, Professional):
        flash("This page is for professionals only", "error")
        return redirect(url_for("main.home"))

    bookings = (
        Appointment.query
        .join(Availability)
        .filter(Availability.professional_id == current_user.id)
        .order_by(Availability.start_time)
        .all()
    )

    now = datetime.now()
    upcoming = [book for book in bookings if book.availability.start_time >= now]
    past = [book for book in bookings if book.availability.start_time <= now]

    return render_template(
    "professional/appointments.html",
                       upcoming=upcoming,
                       past=past,
                       active_page="appointments")


@professional.route("/professional/appointments/<int:appointment_id>/complete", methods=["POST"])
@login_required
def complete_appointment(appointment_id):
    if not isinstance(current_user, Professional):
        flash("This page is for professionals only.", "error")
        return redirect(url_for("main.home"))

    booking = db.session.get(Appointment, appointment_id)

    if booking is None or booking.availability.professional_id != current_user.id:
        flash("Appointment not found.", "error")
        return redirect(url_for("professional.appointments"))

    if booking.status != AppointmentStatus.CONFIRMED:
        flash("Only confirmed appointments can be marked complete.", "error")
        return redirect(url_for("professional.appointments"))

    booking.status = AppointmentStatus.COMPLETED
    db.session.commit()

    flash("Appointment marked complete.", "success")
    return redirect(url_for("professional.appointment"))



@professional.route("/professional/profile", methods=["GET", "POST"])
@login_required
def profile():
    if not isinstance(current_user, Professional):
        flash("This page is for professionals only.", "error")
        return redirect(url_for("main.home"))

    if request.method == "POST":
        firstname = request.form.get("firstname", "").strip()
        lastname = request.form.get("lastname", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        specialty = request.form.get("specialty", "").strip()
        biography = request.form.get("biography", "").strip()

        if not firstname or not lastname or not email or not phone:
            flash("First name, last name, and email and phone are required.", "error")
            return redirect(url_for("professional.profile"))

        if specialty not in SPECIALTIES:
            flash("Please choose a specialty from the list.", "error")
            return redirect(url_for("professional.profile"))

        token = Professional.query.filter(
            Professional.email ==email,
            Professional.id != current_user.id
        ).first()

        if token is not None:
            flash("That email is already in use.", "error")
            return redirect(url_for("professional.profile"))

        current_user.firstname = firstname
        current_user.lastname = lastname
        current_user.email = email
        current_user.phone = phone or None
        current_user.specialty = specialty
        current_user.biography = biography
        db.session.commit()

        flash("Profile updated.", "success")
        return redirect(url_for("professional.profile"))

    return render_template(
        "professional/profile.html",
        specialties=SPECIALTIES,
        active_page="profile",
    )