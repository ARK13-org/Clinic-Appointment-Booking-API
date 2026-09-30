from db.models import Doctor
from schemas import DoctorBase
from sqlalchemy.orm import Session
from db.hash import Hash
from fastapi.exceptions import HTTPException
from fastapi import status

def create_doctor(db: Session, request: DoctorBase):
    doctor = Doctor(
        username=request.username,
        specialization=request.specialization,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor

def get_doctor_by_username(username: str, db: Session):
    doctor = db.query(Doctor).filter(Doctor.username == username).first()
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username '{username}' not found")
    return doctor

def get_doctor_by_specialization(specialization: str, db: Session):
    doctors = db.query(Doctor).filter(Doctor.specialization == specialization).all()
    if not doctors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No doctors found with specialization '{specialization}'")
    return doctors