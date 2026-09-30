from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from auth.oauth2 import get_current_doctor_or_admin
from db import db_availability
from db.database import get_db

from schemas import (
    AvailabilityBase,
    AvailabilityDisplay
)


router = APIRouter(
    prefix="/availability",
    tags=["availability"]
)


@router.post("/")
def create_availability(
    request: AvailabilityBase,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_doctor_or_admin)
):

    return db_availability.create_availability(
        db,
        request.doctor_id,
        request.date
    )


@router.get(
    "/{doctor_id}",
    response_model=list[AvailabilityDisplay]
)
def get_availabilities_by_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):

    return db_availability.get_availabilities_by_doctor(
        db,
        doctor_id
    )

@router.delete("/delete/{availability_id}")
def delete_availability(
    availability_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_doctor_or_admin)
):

    return db_availability.delete_availability_by_id(
        db,
        availability_id
    )

@router.delete("/delete-all/{doctor_id}")
def delete_all_availability_for_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_doctor_or_admin)
):

    return db_availability.delete_all_availability_for_doctor(
        db,
        doctor_id
    )

@router.get("/doctor/{doctor_id}/date/{date}", response_model=list[AvailabilityDisplay])
def get_availabilites_for_doctor_by_date(
    doctor_id: int,
    date: str,
    db: Session = Depends(get_db)
):

    return db_availability.get_availabilities_for_doctor_by_date(
        db,
        doctor_id,
        date
    )