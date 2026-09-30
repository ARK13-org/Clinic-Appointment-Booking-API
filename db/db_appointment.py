from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db.models import (
    Appointment,
    Availability,
    Doctor
)


def create_appointment(
    db: Session,
    patient_id: int,
    availability_id: int
):

    availability = (
        db.query(Availability)
        .filter(
            Availability.id == availability_id
        )
        .first()
    )

    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability not found"
        )

    # Check if the time slot is already booked
    if availability.is_booked:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This appointment time is already booked"
        )

    doctor = (
        db.query(Doctor)
        .filter(
            Doctor.id == availability.doctor_id
        )
        .first()
    )

    if not doctor:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )

    new_appointment = Appointment(
        patient_id=patient_id,
        doctor_username=doctor.username,
        availability_id=availability_id
    )

    # Mark the availability as booked
    availability.is_booked = True

    db.add(new_appointment)

    db.commit()

    db.refresh(new_appointment)

    return {
        "id": new_appointment.id,
        "patient_id": new_appointment.patient_id,
        "doctor_username": new_appointment.doctor_username,
        "date": availability.date,
        "start_time": availability.start_time,
        "end_time": availability.end_time,
        "status": new_appointment.status
    }


def get_appointments_by_patient(
    db: Session,
    patient_id: int
):

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.patient_id == patient_id
        )
        .all()
    )

    return [
        {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_username": appointment.doctor_username,
            "date": appointment.availability.date,
            "start_time": appointment.availability.start_time,
            "end_time": appointment.availability.end_time,
            "status": appointment.status
        }

        for appointment in appointments
    ]

def cancel_appointment(
    db: Session,
    appointment_id: int
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    # Mark the availability as not booked
    availability = (
        db.query(Availability)
        .filter(
            Availability.id == appointment.availability_id
        )
        .first()
    )

    if availability:
        availability.is_booked = False

    db.delete(appointment)
    db.commit()

    return {"detail": "Appointment canceled successfully"}

def reschedule_appointment(
    db: Session,
    appointment_id: int,
    new_availability_id: int
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    new_availability = (
        db.query(Availability)
        .filter(
            Availability.id == new_availability_id
        )
        .first()
    )

    if not new_availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="New availability not found"
        )

    # Check if the new time slot is already booked
    if new_availability.is_booked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This new appointment time is already booked"
        )

    # Mark the old availability as not booked
    old_availability = (
        db.query(Availability)
        .filter(
            Availability.id == appointment.availability_id
        )
        .first()
    )

    if old_availability:
        old_availability.is_booked = False

    # Update the appointment with the new availability
    appointment.availability_id = new_availability_id

    # Mark the new availability as booked
    new_availability.is_booked = True

    db.commit()

    return {"detail": "Appointment rescheduled successfully"}

def get_all_appointments(
    db: Session
):

    appointments = db.query(Appointment).all()

    return [
        {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_username": appointment.doctor_username,
            "date": appointment.availability.date,
            "start_time": appointment.availability.start_time,
            "end_time": appointment.availability.end_time,
            "status": appointment.status
        }

        for appointment in appointments
    ]

def get_appointments_for_doctor_by_date(
    db: Session,
    doctor_username: str,
    date: str
):

    appointments = (
        db.query(Appointment)
        .join(Availability)
        .filter(
            Appointment.doctor_username == doctor_username,
            Availability.date == date
        )
        .all()
    )

    return [
        {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_username": appointment.doctor_username,
            "date": appointment.availability.date,
            "start_time": appointment.availability.start_time,
            "end_time": appointment.availability.end_time,
            "status": appointment.status
        }

        for appointment in appointments
    ]

def get_appointment_by_id(
    db: Session,
    appointment_id: int
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    return {
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_username": appointment.doctor_username,
        "date": appointment.availability.date,
        "start_time": appointment.availability.start_time,
        "end_time": appointment.availability.end_time,
        "status": appointment.status
    }

def get_appointments_status(
    db: Session
):

    appointments = db.query(Appointment).all()

    return [
        {
            "id": appointment.id,
            "patient_id": appointment.patient_id,
            "doctor_username": appointment.doctor_username,
            "date": appointment.availability.date,
            "start_time": appointment.availability.start_time,
            "end_time": appointment.availability.end_time,
            "status": appointment.status
        }

        for appointment in appointments
    ]

def update_appointment_status(
    db: Session,
    appointment_id: int,
    new_status: str
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    appointment.status = new_status

    db.commit()

    return {"detail": "Appointment status updated successfully"}

def get_appointments_status_by_id(
    db: Session,
    appointment_id: int
):

    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )

    return {
        "id": appointment.id,
        "patient_id": appointment.patient_id,
        "doctor_username": appointment.doctor_username,
        "date": appointment.availability.date,
        "start_time": appointment.availability.start_time,
        "end_time": appointment.availability.end_time,
        "status": appointment.status
    }