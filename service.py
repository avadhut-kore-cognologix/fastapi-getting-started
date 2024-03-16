from sqlalchemy.orm import Session

import models, schemas

# get user by user_id
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# get all users
def get_all_users(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.User).offset(skip).limit(limit).all()

# create user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password + "hash"
    db_user = models.User(email = user.email, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    return db_user

# get all notes
def get_all_notes(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Note).offset(skip).limit(limit).all()

# get user notes
def get_user_notes(db: Session, user_id: int):
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()

# create note
def create_note(db: Session, note: schemas.NoteCreate, user_id: int):
    db_note = models.Note(**note.model_dump(), owner_id = user_id)
    db.add(db_note)
    db.commit()
    return db_note