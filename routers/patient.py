from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_admin, get_current_patient_or_admin
from db.database import get_db
from db import db_patient
from schemas import PatientBase , PatientDisplay

router = APIRouter(prefix="/patient", tags=["patient"])

@router.post("", response_model=PatientDisplay)
def create_patient(request: PatientBase, db: Session = Depends(get_db) , current_user=Depends(get_current_patient_or_admin)):
    return db_patient.create_patient(db, request)

@router.get("/{username}", response_model=PatientDisplay)
def get_patient_by_username(username: str, db: Session = Depends(get_db)):
    return db_patient.get_patient_by_username(username, db)

@router.get("", response_model=list[PatientDisplay])
def get_all_patients(db: Session = Depends(get_db)):
    patients = db.query(db_patient.Patient).all()
    return patients

@router.delete("/{username}")
def delete_patient(username: str, db: Session = Depends(get_db) , current_user=Depends(get_current_admin)):
    patient = db_patient.get_patient_by_username(username, db)
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patient with username '{username}' not found")
    db.delete(patient)
    db.commit()
    return {"message": f"Patient with username '{username}' has been deleted"}

@router.delete("")
def delete_all_patients(db: Session = Depends(get_db) , current_user=Depends(get_current_admin)):
    patients = db.query(db_patient.Patient).all()
    if not patients:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No patients found to delete")
    for patient in patients:
        db.delete(patient)
    db.commit()
    return {"message": "All patients have been deleted"}