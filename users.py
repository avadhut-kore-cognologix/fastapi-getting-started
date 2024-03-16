
from fastapi import APIRouter, status, Depends, HTTPException

import models, schemas, service
from db import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model= schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already in use")
    db_user = service.create_user(db, user)
    return db_user

@router.get("/", response_model= list[schemas.User])
def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    users = service.get_all_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model= schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/{user_id}/notes", response_model= schemas.Note, status_code=status.HTTP_201_CREATED)
def create_note(user_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = service.create_note(db, note, user_id)
    return db_note

@router.get("/{user_id}/notes", response_model= list[schemas.Note])
def get_user_notes(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.notes