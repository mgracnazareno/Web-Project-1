# CareSchedule

CareSchedule is a responsive medical appointment scheduling application developed as a full-stack web project. The application enables patients to schedule medical appointments while allowing healthcare professionals to manage their availability and appointments through a secure web interface.

> **Disclaimer:** This is a simulated academic application. All users, appointments, and medical information are fictional and intended for educational purposes only.

---

## Client Need

The client requires a reliable appointment scheduling system that simplifies appointment management for both patients and healthcare professionals. Managing appointments manually often leads to scheduling conflicts, unavailable time slots, and missed appointments.

CareSchedule solves this problem by providing a centralized, database-driven scheduling system where healthcare professionals publish available appointment times and patients can conveniently book appointments online.

---

## Target Users

### Patient
Patients can:
- Register for an account and log in securely
- View available appointment slots
- Book appointments and specify consultation reasons
- View upcoming appointments and historical bookings
- Cancel future appointments
- Manage personal profile details

---

### Healthcare Professional
Healthcare professionals can:
- Register for an account and log in securely
- Manage professional profile details (specialty, office location, bio)
- Publish, edit, or remove available appointment time slots
- View scheduled patient appointments and update booking status
- Manage patient interactions securely

---

## Main Workflow

1. A healthcare professional registers and publishes available appointment slots.
2. A patient registers or logs in to access their dashboard.
3. The patient searches or browses available appointment slots.
4. The patient selects a slot and submits a booking request with a consultation reason.
5. The application validates availability server-side to prevent double booking.
6. The database stores the appointment record and marks the slot as booked.
7. Both patient and healthcare professional dashboards update immediately.

---

## Project Scope & Feature Status (Feature Freeze)

> **Note:** Scope is currently frozen for Deliverable 4 (Feature-Complete Beta). No new major features will be added prior to final submission.

### Must-Have Features (Implemented)
- [x] User registration & authentication (Flask-Login, hashed passwords)
- [x] Role-based authorization & access control (Patient vs. Healthcare Professional)
- [x] Patient Dashboard & Profile Management
- [x] Healthcare Professional Dashboard & Profile Management
- [x] Availability management (Create/Edit/Delete slots)
- [x] Appointment booking & cancellation workflows
- [x] Appointment history tracking
- [x] Server-side data validation & CSRF protection
- [x] Authorization and resource ownership checks
- [x] Fully responsive layout (Bootstrap 5)
- [x] Basic accessibility considerations (semantic HTML, proper form labelling, ARIA attributes)
- [x] Major error handling (404, 500, dynamic flash messages)

### Optional Features
- [ ] Search appointments by specialty / date (Deferred)
- [ ] Profile image uploads (Deferred)
- [ ] English and French localization (Deferred)

---

## Technical Architecture

### Backend
- **Language:** Python
- **Framework:** Flask
- **ORM / Database:** Flask-SQLAlchemy / SQLite
- **Authentication:** Flask-Login, Werkzeug Security

### Frontend
- **Structure / Style:** HTML5, CSS3, Bootstrap 5
- **Templating:** Jinja2 Templates
- **Scripting:** JavaScript (ES6+)

### Development Tools
- **IDEs:** Visual Studio Code / PyCharm
- **Version Control:** Git & GitHub
- **Project Management:** Trello

---

# Database Schema & Relationships

## Database Models

### Patient
Stores authentication details and profile information for patient accounts.

#### Fields
- `id` (`INTEGER`, Primary Key)
- `email` (`VARCHAR(255)`, Unique, Not Null)
- `password_hash` (`VARCHAR(255)`, Not Null)
- `firstname` (`VARCHAR(150)`, Not Null)
- `lastname` (`VARCHAR(150)`, Not Null)
- `phone` (`VARCHAR(20)`, Not Null)
- `dob` (`DATE`, Not Null)

---

### Professional
Stores authentication details and professional profiles for healthcare providers.

#### Fields
- `id` (`INTEGER`, Primary Key)
- `email` (`VARCHAR(255)`, Unique, Not Null)
- `username` (`VARCHAR(255)`, Unique, Not Null)
- `password_hash` (`VARCHAR(255)`, Not Null)
- `firstname` (`VARCHAR(150)`, Nullable)
- `lastname` (`VARCHAR(150)`, Nullable)
- `phone` (`VARCHAR(20)`, Nullable)
- `specialty` (`VARCHAR(150)`, Nullable)
- `biography` (`TEXT`, Nullable)

---

### Availability
Represents available appointment slots published by healthcare professionals.

#### Fields
- `id` (`INTEGER`, Primary Key)
- `professional_id` (`INTEGER`, Foreign Key → `professional.id`, Not Null)
- `start_time` (`DATETIME`, Not Null)
- `end_time` (`DATETIME`, Not Null)
- `is_booked` (`BOOLEAN`, Default: `False`, Not Null)

---

### Appointment
Represents scheduled consultations booked by patients.

#### Fields
- `id` (`INTEGER`, Primary Key)
- `patient_id` (`INTEGER`, Foreign Key → `patient.id`, Not Null)
- `availability_id` (`INTEGER`, Foreign Key → `availability.id`, Unique, Nullable)
- `reason` (`TEXT`, Not Null)
- `status` (`ENUM`: `'confirmed'`, `'cancelled'`, `'completed'`, `'no_show'`, Default: `'confirmed'`, Not Null)
- `scheduled_at` (`DATETIME`, Not Null)

---

## Entity Relationships

- **Patient → Appointment:** One-to-Many (`Patient.appointments` ↔ `Appointment.patient`) with deletion cascade (`all, delete-orphan`).
- **Professional → Availability:** One-to-Many (`Professional.availabilities` ↔ `Availability.professional`).
- **Availability → Appointment:** One-to-One (`Availability.appointment` ↔ `Appointment.availability`).
---

## Installation & Local Setup

Follow these steps to run the application locally:

### Prerequisites
- Python 3.9+ installed
- Git installed

### 1. Clone the Repository
```bash
git clone [https://github.com/mgracnazareno/Web-Project-1.git](https://github.com/mgracnazareno/Web-Project-1.git)
cd Web-Project-1
