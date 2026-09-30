from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_admin
from schemas import AdminBase , AdminDisplay

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/", response_model=AdminDisplay)
def create_admin(request: AdminBase, db: Session = Depends(get_db)):
    return db_admin.create_admin(db, request)

@router.get("/{username}", response_model=AdminDisplay)
def get_admin_by_username(username: str, db: Session = Depends(get_db)):    
    admin = db_admin.get_admin_by_username(username, db)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with username '{username}' not found")
    return admin

@router.delete("/{username}", response_model=AdminDisplay)
def delete_admin(username: str, db: Session = Depends(get_db)):   
    admin = db_admin.get_admin_by_username(username, db)
    if not admin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Admin with username '{username}' not found")
    db.delete(admin)
    db.commit()
    return admin