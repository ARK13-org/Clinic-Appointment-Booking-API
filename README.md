# Clinic Appointment Booking API

A RESTful clinic appointment booking API built with **FastAPI**, **SQLAlchemy**, and **SQLite**. The project provides authentication, role-based authorization, patient and doctor management, doctor availability scheduling, and complete appointment management.

## 🚀 Features

* 🔐 JWT authentication with OAuth2 Password Flow
* 👥 Role-based authorization
* 🧑‍⚕️ Doctor management
* 🧑‍💼 Patient management
* 👨‍💻 Admin management
* 🗓️ Doctor availability management
* ⏰ Automatic hourly availability slots
* 📅 Appointment booking
* ❌ Appointment cancellation
* 🔄 Appointment rescheduling
* 📊 Appointment status management
* 🔎 Search doctors by specialization
* 🔍 Query appointments by patient, doctor, date, ID, or status
* 🔒 Password hashing
* 🗄️ SQLite database with SQLAlchemy ORM
* 📚 Automatic Swagger/OpenAPI documentation
* 📖 ReDoc documentation

## 🛠️ Tech Stack

| Technology | Purpose                     |
| ---------- | --------------------------- |
| Python     | Programming language        |
| FastAPI    | Web framework               |
| SQLAlchemy | ORM and database management |
| SQLite     | Database                    |
| Pydantic   | Data validation and schemas |
| JWT        | Authentication              |
| OAuth2     | Authentication flow         |
| pwdlib     | Password hashing            |
| Uvicorn    | ASGI server                 |

The project uses SQLAlchemy models for patients, doctors, administrators, availability, and appointments.

---

## 📁 Project Structure

```text
Clinic-Appointment-Booking-API/
│
├── main.py
│
├── schemas.py
│
├── routers/
│   ├── patient.py
│   ├── doctors.py
│   ├── admin.py
│   ├── availability.py
│   └── appointment.py
│
├── auth/
│   ├── authentication.py
│   └── oauth2.py
│
├── db/
│   ├── database.py
│   ├── models.py
│   ├── hash.py
│   ├── db_patient.py
│   ├── db_doctors.py
│   ├── db_admin.py
│   ├── db_availability.py
│   └── db_appointment.py
│
├── services/
│   └── availability.py
│
└── Booking.db
```

The project is organized into routers, authentication, database models/data-access modules, services, and Pydantic schemas.

---

# 🔐 Authentication & Authorization

The API uses **JWT access tokens** with the **OAuth2 Password Flow**.

Users authenticate through:

```http
POST /token
```

After successful authentication, the API returns an access token that can be used with:

```http
Authorization: Bearer <access_token>
```

Role-based dependencies are used to control access to protected resources for different user roles.

### Authentication Flow

```text
User
 │
 │ Login
 ▼
POST /token
 │
 ▼
JWT Access Token
 │
 │ Authorization: Bearer <token>
 ▼
Protected Endpoint
 │
 ▼
Role Verification
 │
 ▼
API Response
```

---

# 👥 User Roles

The API contains three main roles:

### Patient

Patients can:

* Create an account
* Access their information
* View available appointments
* Book appointments
* Cancel appointments
* Reschedule appointments
* View their appointments

### Doctor

Doctors can:

* Create a doctor account
* Manage availability
* View appointments
* Search/manage appointments related to their schedule

### Admin

Administrators can:

* Manage users
* Access administrative endpoints
* Manage patients and doctors
* Manage appointment information

---

# 🗄️ Database Models

The project uses SQLAlchemy ORM with SQLite.

### Patient

```text
Patient
├── id
├── username
├── email
└── password
```

A patient can have multiple appointments.

### Doctor

```text
Doctor
├── id
├── username
├── specialization
├── email
└── password
```

A doctor can have multiple availability slots and appointments.

### Admin

```text
Admin
├── id
├── username
├── email
└── password
```

### Availability

```text
Availability
├── id
├── doctor_id
├── date
├── start_time
├── end_time
└── is_booked
```

### Appointment

```text
Appointment
├── id
├── availability_id
├── patient_id
├── doctor_username
└── status
```

## The project defines relationships between patients, doctors, availability slots, and appointments using SQLAlchemy.

# 📅 Appointment System

The appointment workflow is based around doctor availability.

```text
Doctor
   │
   ▼
Create Availability
   │
   ▼
Available Time Slots
   │
   ▼
Patient Selects Slot
   │
   ▼
Create Appointment
   │
   ▼
Slot Marked as Booked
```

When an appointment is created, the selected availability is checked to make sure it exists and is not already booked. The appointment is then created and the availability slot is marked as booked.

Cancellation and rescheduling update the availability state accordingly.

---

# 📡 API Endpoints

## 🔑 Authentication

| Method | Endpoint | Description                            |
| ------ | -------- | -------------------------------------- |
| POST   | `/token` | Authenticate user and obtain JWT token |

---

## 🧑 Patient

| Method | Endpoint              | Description             |
| ------ | --------------------- | ----------------------- |
| GET    | `/patient`            | Get all patients        |
| POST   | `/patient`            | Create patient          |
| DELETE | `/patient`            | Delete all patients     |
| GET    | `/patient/{username}` | Get patient by username |
| DELETE | `/patient/{username}` | Delete patient          |

---

## 🧑‍⚕️ Doctor

| Method | Endpoint                                  | Description                   |
| ------ | ----------------------------------------- | ----------------------------- |
| GET    | `/doctor/`                                | Get all doctors               |
| POST   | `/doctor/`                                | Create doctor                 |
| DELETE | `/doctor/`                                | Delete all doctors            |
| GET    | `/doctor/{username}`                      | Get doctor by username        |
| DELETE | `/doctor/{username}`                      | Delete doctor                 |
| GET    | `/doctor/specialization/{specialization}` | Get doctors by specialization |

---

## 👨‍💼 Admin

| Method | Endpoint            | Description           |
| ------ | ------------------- | --------------------- |
| POST   | `/admin/`           | Create admin          |
| GET    | `/admin/{username}` | Get admin by username |
| DELETE | `/admin/{username}` | Delete admin          |

---

## 🗓️ Availability

| Method | Endpoint                                       | Description                        |
| ------ | ---------------------------------------------- | ---------------------------------- |
| POST   | `/availability/`                               | Create availability                |
| GET    | `/availability/{doctor_id}`                    | Get availabilities by doctor       |
| DELETE | `/availability/delete/{availability_id}`       | Delete availability                |
| DELETE | `/availability/delete-all/{doctor_id}`         | Delete all availability for doctor |
| GET    | `/availability/doctor/{doctor_id}/date/{date}` | Get doctor availability by date    |

---

## 📅 Appointment

| Method | Endpoint                                       | Description                     |
| ------ | ---------------------------------------------- | ------------------------------- |
| POST   | `/appointment/create`                          | Create appointment              |
| GET    | `/appointment/patient/{patient_id}`            | Get appointments by patient     |
| POST   | `/appointment/cancel/{appointment_id}`         | Cancel appointment              |
| POST   | `/appointment/reschedule/{appointment_id}`     | Reschedule appointment          |
| GET    | `/appointment/`                                | Get all appointments            |
| GET    | `/appointment/id/{appointment_id}`             | Get appointment by ID           |
| GET    | `/appointment/doctor/{doctor_username}/{date}` | Get doctor appointments by date |
| GET    | `/appointment/status`                          | Get appointment statuses        |
| GET    | `/appointment/status/{appointment_id}`         | Get appointment status by ID    |
| POST   | `/appointment/update_status/{appointment_id}`  | Update appointment status       |

---

# 🔒 Password Security

User passwords are not stored as plain text.

The project uses `pwdlib` with `PasswordHash.recommended()` to hash passwords before storing them in the database. Password verification is handled through the authentication layer.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Clinic-Appointment-Booking-API.git
cd Clinic-Appointment-Booking-API
```

## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install fastapi uvicorn[standard] sqlalchemy pwdlib python-jose[cryptography] python-multipart
```

## 4. Run the application

```bash
uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

The project uses SQLite for persistence and creates/uses the `Booking.db` database.

---

# 📚 API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

Swagger UI can be used to test endpoints directly from the browser.

---

# 🧪 Example API Workflow

A typical booking flow looks like this:

```text
1. Create Patient
       │
       ▼
2. Create Doctor
       │
       ▼
3. Doctor Creates Availability
       │
       ▼
4. Patient Authenticates
       │
       ▼
5. Patient Views Available Slots
       │
       ▼
6. Patient Creates Appointment
       │
       ▼
7. Availability Becomes Booked
       │
       ▼
8. Appointment Can Be Viewed,
   Cancelled, Rescheduled,
   or Its Status Updated
```

---

# 🧩 What This Project Demonstrates

This project demonstrates practical backend development concepts including:

* REST API development
* FastAPI routing
* Dependency injection
* SQLAlchemy ORM
* Database relationships
* Pydantic schemas
* JWT authentication
* OAuth2 Password Flow
* Role-based authorization
* Password hashing
* CRUD operations
* Appointment business logic
* Availability management
* Request validation
* Response validation
* Modular backend architecture
* Interactive API documentation

---

# 📌 Project Highlights

The main focus of this project is implementing a complete appointment-booking backend rather than a simple CRUD API.

It combines:

```text
Authentication
      +
Authorization
      +
Database
      +
Doctor Availability
      +
Appointment Management
      =
Clinic Appointment Booking API
```

---

---

## 👨‍💻 Developer

**Alireza Koupaei**
