
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import models, schemas, service
from db import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already in use")
    db_user = service.create_user(db, user)
    access_token = await service.create_acces_token(db_user.id, db_user.email)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.email
    }

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = await service.authenticate(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect username or password")
    access_token = await service.create_acces_token(db_user.id, db_user.email)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile", response_model=schemas.User)
async def get_current_user(token: str, db: Session = Depends(get_db)):
    db_user = await service.get_current_user(db, token)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authenticated")
    return db_user

@router.put("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(username: str, token: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = await service.get_current_user(db, token)
    if not db_user or db_user.email != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this user")
    db_user = service.update_user(db, db_user, user)

@router.get("/resetpassword/sendcode/{email}")
async def send_reset_password_code(email: str, db: Session = Depends(get_db)):
    db_user = service.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User with email id not found")
    code = await service.generate_code(db, email)
    await service.fake_email_send(email, code)
    return code

@router.get("/resetpassword/verifycode")
async def verify_reset_password_code(email: str, code: str, db: Session = Depends(get_db)):
    return await service.verify_code(db, email, code)

@router.put("/resetpassword/reset", status_code=status.HTTP_204_NO_CONTENT)
async def send_reset_password_code(email: str, password: str, db: Session = Depends(get_db)):
    db_user = service.get_user_by_email(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User with email id not found")
    service.update_password(db, db_user, password)
    

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