# CareSchedule

CareSchedule is a responsive medical appointment scheduling application developed as a five-week academic web project. It allows healthcare professionals to publish available appointment times and allows patients to find, book, view, and cancel appointments.

> This is a simulated academic application. It must use fictional demonstration accounts and fictional medical information only.

## Client Need

The client needs a reliable system that helps patients and healthcare professionals manage appointments. When scheduling is handled manually, patients may not know which times are available and healthcare professionals may receive overlapping requests.

CareSchedule addresses this problem by providing one database-backed source for availability and appointments.

## Target Users

### Patient

The primary user is a patient who wants to:

- create an account and log in;
- view available appointment times;
- book an appointment;
- provide a reason for the consultation;
- view upcoming appointments; and
- cancel a future appointment.

### Healthcare Professional

The secondary user is a healthcare professional who wants to:

- create an account and log in;
- publish available appointment times;
- manage their own availability; and
- view appointments booked by patients.

## Main Workflow

1. A healthcare professional creates an available time slot.
2. A patient views the open appointment times.
3. The patient selects a slot and submits the booking form.
4. The server validates the request and confirms that the slot is still available.
5. The appointment is saved in the database.
6. The patient and healthcare professional dashboards display the updated information.

## Project Scope

### Must-Have Features

- Patient and healthcare professional registration
- Login and logout
- Role-based dashboards
- Availability creation and management
- Appointment search and booking
- Appointment viewing and cancellation
- Server-side validation
- Authorization and ownership checks
- Success, error, loading, and empty states
- Responsive and accessible interface

### Optional Features

Optional features will only be considered after the main workflow is complete:

- Search filters by specialty or date
- Availability editing
- Appointment status filters
- English and French interface

### Out of Scope

The five-week version will not include:

- clinic accounts or clinic administration;
- a complete administrator dashboard;
- medical records or document sharing;
- live chat or a chatbot;
- real email or SMS reminders;
- billing, payments, or insurance validation; or
- location-based clinic search.

## Planned Technology

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite

### Frontend

The frontend track will be finalized before implementation:

- **Track A:** Jinja templates, HTML, CSS or Bootstrap, and JavaScript; or
- **Track B:** React frontend connected to a Flask JSON API.

### Development Tools

- Figma for UX/UI design
- Trello for project management
- Git and GitHub for version control

## Proposed Database Models

### User

Represents patient and healthcare professional accounts.

Important fields:

- `id`
- `first_name`
- `last_name`
- `email`
- `password_hash`
- `role`
- `specialty`

### Availability

Represents an appointment time published by a healthcare professional.

Important fields:

- `id`
- `doctor_id`
- `start_time`
- `end_time`
- `is_booked`

### Appointment

Represents a booking made by a patient.

Important fields:

- `id`
- `patient_id`
- `availability_id`
- `reason`
- `description`
- `status`
- `created_at`

## Proposed Relationships

- One healthcare professional can create many availability records.
- One patient can have many appointments.
- One availability record can have zero or one appointment.

## Project Documentation

Project documents will be stored in the `docs` directory:

```text
docs/
├── diagrams/
├── figma/
├── journal/
├── presentations/
└── trello/
```

## Project Links

- **Figma Design:** In progress
- [Trello Board](https://trello.com/invite/b/6a697834197cdd9d1ce1bf92/ATTI49527a5f964be3d9250d3331b7491f8d6918B42E/web-project-1)
- [GitHub Repository](https://github.com/mgracnazareno/Web-Project-1)

## Installation

Installation instructions will be added during backend development.

The final instructions will explain how to:

1. clone the repository;
2. create and activate a virtual environment;
3. install the dependencies;
4. configure environment variables;
5. create the database; and
6. run the application.

## Project Status

The project is currently in **Week 1: Definition and Design**.

Current work includes:

- defining the client need and target users;
- controlling the project scope;
- planning the primary workflow;
- creating the Figma design;
- planning the database and routes;
- creating the use case diagram; and
- preparing the initial repository.

## Privacy and Security

- Only fictional demonstration data will be used.
- Passwords will be securely hashed.
- Real passwords, API keys, and secrets will not be committed.
- The `.env` file and local database will be excluded using `.gitignore`.
- Authorization checks will prevent users from modifying records they do not own.

## Author

**[Mary Grace Nazareno]**

Course: **[582-32W-VA]**


