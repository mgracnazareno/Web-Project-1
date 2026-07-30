# CareSchedule

CareSchedule is a responsive medical appointment scheduling application developed as part of a five-week academic web development project. The application enables patients to schedule medical appointments while allowing healthcare professionals to manage their availability and appointments through a secure web interface.

> **Disclaimer:** This is a simulated academic application. All users, appointments, and medical information are fictional and are intended for educational purposes only.

---

# Client Need

The client requires a reliable appointment scheduling system that simplifies appointment management for both patients and healthcare professionals. Managing appointments manually often leads to scheduling conflicts, unavailable time slots, and missed appointments.

CareSchedule solves this problem by providing a centralized, database-driven scheduling system where healthcare professionals publish available appointment times and patients can conveniently book appointments online.

---

# Target Users

## Patient

Patients can:

- Register for an account
- Log in securely
- View available appointment slots
- Book appointments
- Provide a reason for the consultation
- View upcoming appointments
- View appointment history
- Cancel future appointments
- Manage their personal profile

---

## Healthcare Professional

Healthcare professionals can:

- Register for an account
- Log in securely
- Manage their professional profile
- Publish available appointment times
- Edit or remove availability
- View scheduled appointments
- Manage patient bookings

---

# Main Workflow

1. A healthcare professional registers and publishes available appointment slots.
2. A patient registers or logs in.
3. The patient browses available appointment times.
4. The patient selects an appointment and submits a booking request.
5. The application validates that the selected appointment is still available.
6. The appointment is stored in the database.
7. The patient and healthcare professional dashboards are automatically updated.

---

# Project Scope

## Must-Have Features

- User registration
- Login and logout
- Role-based authentication
- Patient dashboard
- Healthcare professional dashboard
- Profile management
- Appointment booking
- Appointment cancellation
- Appointment history
- Availability management
- Server-side validation
- Authorization and ownership checks
- Responsive design
- Accessibility considerations

---

## Optional Features

The following features may be implemented if time permits:

- Search appointments by specialty
- Search appointments by date
- Appointment filtering
- English and French localization
- Profile image uploads

---

## Out of Scope

The academic version will **not** include:

- Multiple clinics
- Administrator dashboard
- Medical records
- File uploads
- Online payments
- Insurance processing
- Email reminders
- SMS notifications
- Video consultations
- AI chatbot

---

# Planned Technology

## Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- SQLite

---

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Jinja Templates

---

## Development Tools

- Figma
- Trello
- Git
- GitHub
- Visual Studio Code

---

# Proposed Database Models

## User

Stores authentication information for every account.

### Fields

- id
- email
- password_hash
- role *(patient or healthcare_professional)*
- created_at

---

## Patient

Stores patient information.

### Fields

- id
- user_id *(FK → User.id)*
- first_name
- last_name
- phone
- date_of_birth

---

## HealthcareProfessional

Stores healthcare professional information.

### Fields

- id
- user_id *(FK → User.id)*
- first_name
- last_name
- specialty
- phone
- office_location
- biography

---

## Availability

Represents appointment slots created by healthcare professionals.

### Fields

- id
- healthcare_professional_id *(FK → HealthcareProfessional.id)*
- start_time
- end_time
- is_booked

---

## Appointment

Represents appointments booked by patients.

### Fields

- id
- patient_id *(FK → Patient.id)*
- availability_id *(FK → Availability.id)*
- reason
- description
- status
- created_at

---

# Proposed Relationships

- One User has one Patient profile or one Healthcare Professional profile.
- One Healthcare Professional can create many Availability records.
- One Healthcare Professional can receive many Appointments through their Availability records.
- One Patient can book many Appointments.
- One Availability record can be associated with zero or one Appointment.

---

# Planned Pages

## Public Pages

- Home
- Login
- Register

---

## Patient Pages

- Dashboard
- Book Appointment
- My Appointments
- Appointment History
- Patient Profile

---

## Healthcare Professional Pages

- Dashboard
- Manage Availability
- Manage Appointments
- Healthcare Professional Profile

---

# UI Design

The user interface is being designed in **Figma** following a user-centered design process.

### Ready

- Information architecture
- Low-fidelity wireframes
- High-fidelity mockups
- User flow planning
- Desktop layouts

### Upcoming

- Interactive prototype
- Mobile responsive layouts
- Component library

---

# Project Documentation

```text
docs/
├── diagrams/
│   ├── use-case-diagram.pdf
│   ├── class-diagram.pdf
│   └── er-diagram.pdf
│
├── figma/
│   ├── low-fidelity/
│   ├── high-fidelity/
│   └── prototype-link.md
│
├── journal/
│   ├── journal.md
│   └── project-design-journal.pdf
│
├── presentations/
│
├── trello/
│
└── weeks/
    ├── week-0-definition-design/
    ├── week-1/
    ├── week-2/
    ├── week-3/
    ├── week-4/
    └── week-5/
```

---

# Project Links

- **Figma Prototype:** Coming Soon
- **Trello Board:** https://trello.com/invite/b/6a697834197cdd9d1ce1bf92/ATTI49527a5f964be3d9250d3331b7491f8d6918B42E/web-project-1
- **GitHub Repository:** https://github.com/mgracnazareno/Web-Project-1

---

# Installation

Installation instructions will be completed during the implementation phase.

The final guide will explain how to:

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install project dependencies.
4. Configure environment variables.
5. Initialize the database.
6. Run the Flask application locally.

---

# Project Status

## Current Phase

**Week 1 — Definition & Design**

### Completed

- Client requirements analysis
- Target audience definition
- Project scope planning
- Primary workflow design
- Initial database design
- Entity relationship planning
- Use Case Diagram
- Class Diagram
- Low-fidelity wireframes
- High-fidelity mockups
- GitHub repository
- Trello board
- Project journal
- README documentation

### In Progress

- Interactive Figma prototype
- Flask project setup
- SQLAlchemy models
- Authentication system
- Initial page templates

### Upcoming

- CRUD functionality
- Appointment booking
- Availability management
- Responsive implementation
- Testing
- Deployment
- Final presentation

---

# Future Improvements

Possible future enhancements include:

- Email appointment reminders
- SMS notifications
- Google Calendar integration
- Doctor profile pictures
- Medical history management
- Online consultations
- Mobile application
- Administrator dashboard
- Clinic management
- Analytics dashboard

---

# Privacy and Security

- Only fictional demonstration data will be used.
- Passwords will be securely hashed.
- Sensitive configuration values will be stored in environment variables.
- The `.env` file and SQLite database will be excluded using `.gitignore`.
- Authorization checks will ensure users can only access or modify records they own.
- User authentication will be implemented using Flask-Login.

---

# Author

**Mary Grace Nazareno**

**Course:** 582-32W-VA — Web Project 1

**Institution:** Vanier College

**Semester:** Summer 2026
