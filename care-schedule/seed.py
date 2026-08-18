from datetime import date, datetime, time, timedelta

from bp_app.app import app
from bp_app.models import (
    db,
    Patient,
    Professional,
    Availability,
    Appointment,
    AppointmentStatus,
)

DEMO_PASSWORD = "Password123!"
SLOT_HOURS = [9, 10, 11, 14, 15]


def reset_database():
    db.drop_all()
    db.create_all()


def create_professionals():
    rows = [
        ("evasquez", "e.vasquez@careschedule.test", "Elena", "Vasquez",
         "514-555-0110", "Cardiology",
         "Cardiologist with 15 years of hospital practice."),
        ("mdubois", "m.dubois@careschedule.test", "Marc", "Dubois",
         "438-555-0121", "Family Medicine",
         "Family physician focused on preventive care."),
        ("aosei", "a.osei@careschedule.test", "Ama", "Osei",
         "514-555-0132", "Dermatology",
         "Dermatologist specializing in skin cancer screening."),
    ]

    professionals = []
    for username, email, firstname, lastname, phone, specialty, biography in rows:
        pro = Professional(
            username=username,
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            specialty=specialty,
            biography=biography,
        )
        pro.set_password(DEMO_PASSWORD)
        db.session.add(pro)
        professionals.append(pro)

    db.session.flush()
    return professionals


def create_patients():
    rows = [
        ("joan.smith@email.test", "Joan", "Smith", "514-555-0142", date(1988, 3, 14)),
        ("liam.tremblay@email.test", "Liam", "Tremblay", "438-555-0198", date(1975, 11, 2)),
        ("priya.raman@email.test", "Priya", "Raman", "514-555-0173", date(1996, 7, 21)),
    ]

    patients = []
    for email, firstname, lastname, phone, dob in rows:
        patient = Patient(
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            dob=dob,
        )
        patient.set_password(DEMO_PASSWORD)
        db.session.add(patient)
        patients.append(patient)

    db.session.flush()
    return patients


def create_availability(professionals):
    today = date.today()
    slots = {pro.id: [] for pro in professionals}

    for day_offset in range(-7, 15):
        day = today + timedelta(days=day_offset)
        if day.weekday() >= 5:
            continue

        for pro in professionals:
            for hour in SLOT_HOURS:
                start = datetime.combine(day, time(hour, 0))
                slot = Availability(
                    professional_id=pro.id,
                    start_time=start,
                    end_time=start + timedelta(minutes=45),
                )
                db.session.add(slot)
                slots[pro.id].append(slot)

    db.session.flush()
    return slots


def book(patient, slot, reason, status):
    appointment = Appointment(
        reason=reason,
        status=status,
        scheduled_at=slot.start_time,
        patient_id=patient.id,
        availability_id=slot.id,
    )
    slot.is_booked = True
    db.session.add(appointment)
    return appointment


def cancel(appointment, slot):
    appointment.status = AppointmentStatus.CANCELLED
    appointment.availability_id = None
    slot.is_booked = False


def create_appointments(patients, slots_by_professional):
    joan, liam, priya = patients
    now = datetime.now()

    all_slots = [slot for slots in slots_by_professional.values() for slot in slots]
    upcoming = sorted([s for s in all_slots if s.start_time > now], key=lambda s: s.start_time)
    past = sorted([s for s in all_slots if s.start_time < now], key=lambda s: s.start_time)

    book(joan, upcoming[0], "Annual heart check-up", AppointmentStatus.CONFIRMED)
    book(joan, upcoming[12], "Follow-up on blood pressure", AppointmentStatus.CONFIRMED)
    book(joan, past[3], "Chest pain assessment", AppointmentStatus.COMPLETED)

    cancelled_slot = upcoming[25]
    cancel(book(joan, cancelled_slot, "Skin rash consultation", AppointmentStatus.CONFIRMED),
           cancelled_slot)

    book(liam, upcoming[5], "Persistent cough", AppointmentStatus.CONFIRMED)
    book(liam, past[8], "Vaccination", AppointmentStatus.COMPLETED)
    book(priya, upcoming[8], "Mole screening", AppointmentStatus.CONFIRMED)
    book(priya, past[15], "Missed appointment", AppointmentStatus.NO_SHOW)


def summary():
    print("Seed complete.")
    print(f"  professionals : {Professional.query.count()}")
    print(f"  patients      : {Patient.query.count()}")
    print(f"  slots         : {Availability.query.count()}")
    print(f"  appointments  : {Appointment.query.count()}")
    print()
    print(f"Password for every demo account: {DEMO_PASSWORD}")
    print("  professionals : e.vasquez@ / m.dubois@ / a.osei@careschedule.test")
    print("  patients      : joan.smith@ / liam.tremblay@ / priya.raman@email.test")


def main():
    with app.app_context():
        reset_database()
        professionals = create_professionals()
        patients = create_patients()
        slots = create_availability(professionals)
        create_appointments(patients, slots)
        db.session.commit()
        summary()


if __name__ == "__main__":
    main()