from fastapi import APIRouter, status, Depends, HTTPException

import models, schemas, service
from db import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model= list[schemas.Note])
def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    notes = service.get_all_notes(db, skip=skip, limit=limit)
    return notes