from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db import models
from db.hash import Hash
from db.database import get_db
from auth import oauth2


router = APIRouter(tags=["authentication"])


@router.post("/token")
def get_token(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Check Patient
    user = (
        db.query(models.Patient)
        .filter(models.Patient.username == request.username)
        .first()
    )

    if user:
        if not Hash.verify(user.password, request.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        role = "patient"

    else:
        # Check Admin
        user = (
            db.query(models.Admin)
            .filter(models.Admin.username == request.username)
            .first()
        )

        if user:
            if not Hash.verify(user.password, request.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )

            role = "admin"

        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

    access_token = oauth2.create_access_token(
        data={
            "sub": user.username,
            "role": role
        }
    )

    return {
        "access_token": access_token,
        "type_token": "bearer",
        "userID": user.id,
        "username": user.username,
        "role": role
    }