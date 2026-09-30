from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from auth.oauth2 import get_current_admin, get_current_patient_or_admin
from db import db_appointment
from db.database import get_db

from schemas import (
    AppointmentBase,
    AppointmentDisplay
)


router = APIRouter(
    prefix="/appointment",
    tags=["appointment"]
)


@router.post(
    "/create",
    response_model=AppointmentDisplay
)
def create_appointment(
    appointment: AppointmentBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_patient_or_admin)
):

    return db_appointment.create_appointment(
        db=db,
        patient_id=appointment.patient_id,
        availability_id=appointment.availability_id
    )


@router.get(
    "/patient/{patient_id}",
    response_model=list[AppointmentDisplay]
)
def get_appointments_by_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    return db_appointment.get_appointments_by_patient(
        db=db,
        patient_id=patient_id
    )

@router.post("/cancel/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_patient_or_admin)
):
    return db_appointment.cancel_appointment(
        db=db,
        appointment_id=appointment_id
    )

@router.post("/reschedule/{appointment_id}")
def reschedule_appointment(
    appointment_id: int,
    new_availability_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_patient_or_admin)
):
    return db_appointment.reschedule_appointment(
        db=db,
        appointment_id=appointment_id,
        new_availability_id=new_availability_id
    )

@router.get("/", response_model=list[AppointmentDisplay])
def get_all_appointments(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    return db_appointment.get_all_appointments(db=db)

@router.get("/id/{appointment_id}", response_model=AppointmentDisplay)
def get_appointment_by_id(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    return db_appointment.get_appointment_by_id(
        db=db,
        appointment_id=appointment_id
    )

@router.get('/doctor/{doctor_username}/{date}', response_model=list[AppointmentDisplay])
def get_appointments_for_doctor_by_date(
    doctor_username: str,
    date: str,
    db: Session = Depends(get_db),
):
    return db_appointment.get_appointments_for_doctor_by_date(
        db=db,
        doctor_username=doctor_username,
        date=date
    )

@router.get("/status", response_model=list[AppointmentDisplay])
def get_appointments_status(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    return db_appointment.get_appointments_status(db=db)

@router.get("/status/{appointment_id}", response_model=AppointmentDisplay)
def get_appointments_status_by_id(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    return db_appointment.get_appointments_status_by_id(
        db=db,
        appointment_id=appointment_id
    )

@router.post("/update_status/{appointment_id}")
def update_appointment_status(
    appointment_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin)
):
    return db_appointment.update_appointment_status(
        db=db,
        appointment_id=appointment_id,
        new_status=new_status
    )