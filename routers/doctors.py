from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_admin, get_current_doctor, get_current_doctor_or_admin
from db.database import get_db
from db import db_doctors
from schemas import DoctorBase, DoctorBasicDisplay , DoctorDisplay

router = APIRouter(prefix="/doctor", tags=["doctor"])

@router.post("/", response_model=DoctorDisplay)
def create_doctor(request: DoctorBase, db: Session = Depends(get_db) , current_user=Depends(get_current_doctor_or_admin)):
    return db_doctors.create_doctor(db, request)

@router.get("/{username}", response_model=DoctorDisplay)
def get_doctor_by_username(username: str, db: Session = Depends(get_db)):
    doctor = db_doctors.get_doctor_by_username(username, db)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username '{username}' not found")
    return doctor

@router.get("/", response_model=list[DoctorBasicDisplay])
def get_all_doctors(db: Session = Depends(get_db)):
    doctors = db.query(db_doctors.Doctor).all()
    return doctors

@router.delete("/{username}", response_model=DoctorDisplay)
def delete_doctor(username: str, db: Session = Depends(get_db) , current_user=Depends(get_current_doctor_or_admin)):
    doctor = db_doctors.get_doctor_by_username(username, db)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username '{username}' not found")
    db.delete(doctor)
    db.commit()
    return doctor

@router.delete("/", response_model=list[DoctorDisplay])
def delete_all_doctors(db: Session = Depends(get_db) , current_user=Depends(get_current_admin)):
    doctors = db.query(db_doctors.Doctor).all()
    for doctor in doctors:
        db.delete(doctor)
    db.commit()
    return doctors

@router.get("/specialization/{specialization}", response_model=list[DoctorBasicDisplay])
def get_doctor_by_specialization(specialization: str, db: Session = Depends(get_db)):
    doctors = db_doctors.get_doctor_by_specialization(specialization, db)
    if not doctors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No doctors found with specialization '{specialization}'")
    return doctors