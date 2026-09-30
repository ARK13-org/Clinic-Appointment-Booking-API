from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta

from jose import jwt
from jose.exceptions import JWTError

from sqlalchemy.orm import Session

from db.database import get_db
from fastapi.exceptions import HTTPException
from fastapi import Depends, status

from db import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


SECRET_KEY = "..."
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    error_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if not username or not role:
            raise error_credentials

    except JWTError:
        raise error_credentials

    if role == "patient":
        user = (
            db.query(models.Patient)
            .filter(models.Patient.username == username)
            .first()
        )

    elif role == "admin":
        user = (
            db.query(models.Admin)
            .filter(models.Admin.username == username)
            .first()
        )

    else:
        raise error_credentials

    if not user:
        raise error_credentials

    return user


def get_current_patient(
    current_user=Depends(get_current_user)
):
    if not isinstance(current_user, models.Patient):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patients are allowed"
        )

    return current_user


def get_current_admin(
    current_user=Depends(get_current_user)
):
    if not isinstance(current_user, models.Admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins are allowed"
        )

    return current_user


def get_current_patient_or_admin(
    current_user=Depends(get_current_user)
):
    if not isinstance(current_user, (models.Patient, models.Admin)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only patients and admins are allowed"
        )

    return current_user

def get_current_doctor(
    current_user=Depends(get_current_user)
):
    if not isinstance(current_user, models.Doctor):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors are allowed"
        )

    return current_user

def get_current_doctor_or_admin(
    current_user=Depends(get_current_user)
):
    if not isinstance(current_user, (models.Doctor, models.Admin)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only doctors and admins are allowed"
        )

    return current_user