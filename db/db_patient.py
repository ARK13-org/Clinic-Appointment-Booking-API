from db.models import Patient
from schemas import PatientBase
from sqlalchemy.orm import Session
from db.hash import Hash
from fastapi.exceptions import HTTPException
from fastapi import status

def create_patient(db: Session, request: PatientBase):
    patient = Patient(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient

def get_patient_by_username(username: str, db: Session):
    patient = db.query(Patient).filter(Patient.username == username).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username '{username}' not found")
    return patient
