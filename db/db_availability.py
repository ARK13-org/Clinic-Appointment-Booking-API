from datetime import date

from sqlalchemy.orm import Session

from db.models import Availability
from services.availability import generate_time_slots


def create_availability(
    db: Session,
    doctor_id: int,
    selected_date: date
):
    slots = generate_time_slots()

    for slot in slots:

        availability = Availability(
            doctor_id=doctor_id,
            date=selected_date,
            start_time=slot["start_time"],
            end_time=slot["end_time"],
            is_booked=False
        )

        db.add(availability)

    db.commit()

    return {
        "message": "Availability created successfully"
    }


def get_availabilities(db: Session):

    return (
        db.query(Availability)
        .filter(
            Availability.is_booked == False
        )
        .all()
    )


def get_availabilities_by_doctor(
    db: Session,
    doctor_id: int
):

    return (
        db.query(Availability)
        .filter(
            Availability.doctor_id == doctor_id,
            Availability.is_booked == False
        )
        .all()
    )

def get_availability_by_id(
    db: Session,
    availability_id: int
):

    return (
        db.query(Availability)
        .filter(Availability.id == availability_id)
        .first()
    )

def delete_availability_by_id(
    db: Session,
    availability_id: int
):

    availability = get_availability_by_id(db, availability_id)

    if not availability:
        return {
            "message": "Availability not found"
        }

    db.delete(availability)
    db.commit()

    return {
        "message": "Availability deleted successfully"
    }

def delete_all_availability_for_doctor(
    db: Session,
    doctor_id: int
):
    availabilities = (
        db.query(Availability)
        .filter(Availability.doctor_id == doctor_id)
        .all()
    )

    if not availabilities:
        return {
            "message": "No availability found for the doctor"
        }

    for availability in availabilities:
        db.delete(availability)

    db.commit()

    return {
        "message": "All availability deleted successfully for the doctor"
    }

def get_availabilities_for_doctor_by_date(
    db: Session,
    doctor_id: int,
    selected_date: date
):

    return (
        db.query(Availability)
        .filter(
            Availability.doctor_id == doctor_id,
            Availability.date == selected_date,
            Availability.is_booked == False
        )
        .all()
    )