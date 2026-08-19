# WEB PROJECT 1

## Project Design Journal

**Student:** Mary Grace Nazareno  
**Course:** 582-32W-VA  
**Instructor:** Kamyar Karimi  
**Project:** Medical Appointment Scheduling System  
**Semester:** Summer 2026

---

## July 27, 2026

### Initial Planning

Today is the start of our Web Project 1 and we had our introduction of what to achieve and what to expect.

After the class, I started conceptualizing what kind of project I will build. The initial phase is always the hardest. I have a few options: I was thinking of building a job tracker, a medical appointment scheduling application or e-commerce.

To wrap things up, I spent the rest of the time researching for inspiration.

---

## July 28, 2026

### Defining the Project Scope

I decided to build a medical appointment scheduling application. At first, I felt unsure about what features to include, so I used the inspiration I found yesterday as a starting point and will build it from there.

The initial core features will include user authentication (login and logout), the patient’s portal for booking and viewing appointments, and interface for medical professionals to manage appointment requests and schedules. While I have not finalized every feature, I expect additional ideas and improvements to emerge as I continue designing and implementing the system.

Here is the link of the case study where I based my project. Although I am not building all that is written on it. I just want to share that this is where I got my ideas from. I haven’t build it and I am using this project to use the learned skills to build it.

### Case Study Source

[View the Case Study PDF](https://docs.google.com/document/d/e/2PACX-1vSHBr7C2XWPPeIRy_hvsEzhiuq4J_Q2qwS2EYXGOSNdqW8bw_PTmbpAyFgkVI2SRc-lW4tONwaI-SFc/pub)

---

## July 29, 2026

### System Planning

Today, I reviewed the project requirements to ensure that my application meets each one. The most challenging part so far has been the Figma design. I don't think three days is enough to create a complete low-fidelity wireframe, so for now I am focusing on planning the application's structure instead. I identified the main pages that the system will need, including the Home page, Login page, Patient Portal, and Medical Professional dashboard. Although I have not created the wireframes yet, having these pages planned gives me a clear direction for the next stage of the project.

I also designed the initial database structure. At this stage, I am keeping it relatively simple since the application only needs to demonstrate the required functionality. In a real-world medical appointment scheduling system, the database would typically be much more complex, with multiple related tables for patients, healthcare professionals, appointments, availability, medical records, and other supporting data. For this project, however, I am focusing on a clean and manageable database design that meets the course requirements while leaving room for future enhancements.

## August 3, 2026
Figma Design
I started working on my Figma design. The layout is mostly identical to other pages so it is easier to create. The only page that differs is the home page and the rest are alike. My design is minimalistic, straight forward and user-friendly.
The only reason that blocks me from completing this task is that I have a wedding party to attend today which means I’ll be away for the whole day..

## August 4, 2026
After the demo class today, I continued working on my Figma design. Then, I reviewed  the  materials from our Python & JavaScript class to refresh my understanding of how to implement CRUD and the DOM. I redid some of the labs we had to recall the techniques before I began working on my backend.


## August 5, 2026
I began working on the core structure of the backend. I did the full patient authentication, added the login route, organized the project by registering the main blueprint and organized the app into a cleaner layout. I created the models needed for my application. I added the necessary relationships.


## August 6, 2026
I am always looking forward to our presentation day because I learn a lot from other students. The ideas are impressive.

## Development Progress Summary

### August 13, 2026
Focused on building the patient dashboard and appointment booking workflow.

- Created the patient dashboard page and layout.
- Added patient sidebar navigation.
- Made the dashboard sidebar reusable and overridable.
- Built the patient dashboard route.
- Added professional selection to the appointment booking route.
- Created the appointment booking page.
- Fixed the professional add-slot modal template.

---

### August 14, 2026
Focused on improving the professional dashboard and displaying availability data.

- Added queries for today's and upcoming professional availability slots.
- Rendered dashboard information using data passed from Flask routes.
- Added an empty state when a professional has no available slots.
- Merged recent development changes into the `master` branch.

---

### August 17, 2026
Focused on expanding the patient dashboard, appointment history, profiles, and authentication structure.

- Updated models to support appointment history queries.
- Created an appointment history page for patients.
- Added an appointment history link to the patient sidebar.
- Separated upcoming visits from past visits on the patient dashboard.
- Added profile validation.
- Separated patient registration validation into its own validator.
- Fixed appointment history card markup.
- Connected the sidebar to history and profile pages.
- Added a shared authentication blueprint.
- Stopped tracking the development database in Git.

---

### August 18, 2026
Focused on improving appointment management, professional search, availability, and the booking experience.

- Added professional search and filtering to the appointment booking page.
- Styled the patient's **My Appointments** page.
- Added a link from registration to the role-selection page.
- Fixed the specialty dropdown so empty values are handled correctly.
- Added a phone field for professional accounts.
- Added a database seed script for development/testing data.
- Made the appointment slot list scrollable with sticky date headings.
- Made the dashboard sidebar remain in place while scrolling.
- Changed appointment booking to use a confirmation modal instead of a separate page.
- Styled the patient reschedule page with a scrollable slot panel and selection footer.
- Fixed the collapsed sidebar so it maintains the correct narrow width.
- Updated and expanded the README documentation for better clarity.


