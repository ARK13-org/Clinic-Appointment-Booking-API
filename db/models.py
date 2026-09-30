from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Boolean
from sqlalchemy.orm import relationship

from db.database import base


class Patient(base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)

    appointments = relationship(
        "Appointment",
        back_populates="patient"
    )


class Doctor(base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    specialization = Column(String)
    email = Column(String)
    password = Column(String)

    availabilities = relationship(
        "Availability",
        back_populates="doctor"
    )

    appointments = relationship(
        "Appointment",
        back_populates="doctor",
        foreign_keys="Appointment.doctor_username"
    )


class Admin(base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


class Availability(base):
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False
    )

    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    # False = available
    # True = booked
    is_booked = Column(
        Boolean,
        default=False,
        nullable=False
    )

    doctor = relationship(
        "Doctor",
        back_populates="availabilities"
    )

    appointments = relationship(
        "Appointment",
        back_populates="availability"
    )


class Appointment(base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True, index=True)

    availability_id = Column(
        Integer,
        ForeignKey("availabilities.id"),
        nullable=False
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    doctor_username = Column(
        String,
        ForeignKey("doctors.username"),
        nullable=False
    )
    
    status = Column(String, default="booked")

    availability = relationship(
        "Availability",
        back_populates="appointments"
    )

    patient = relationship(
        "Patient",
        back_populates="appointments"
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments",
        foreign_keys=[doctor_username]
    )