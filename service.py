from random import randint
from sqlalchemy.orm import Session

import models, schemas
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta, datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
EXPIRES_MINUTES = 60 * 24 # 1 day

oaut2_bearer = OAuth2PasswordBearer(tokenUrl="token") # localhost:8000/token
bcrypt_context = CryptContext(schemes=["bcrypt"])

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
    hashed_password = bcrypt_context.hash(user.password)
    db_user = models.User(email = user.email, hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    return db_user

# Update user
def update_user(db: Session, db_user: models.User, user_update: schemas.UserUpdate):
    db_user.email = user_update.email or db_user.email
    db.commit()
    db.refresh(db_user)
    return db_user

# Update password
def update_password(db: Session, db_user: models.User, password: str):
    db_user.hashed_password = bcrypt_context.hash(password)
    db.commit()

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

# create token
# jwt = {encoded_data, secret_key, algorithm}
async def create_acces_token(id: int, email: str):
    encode = {"sub": email, "id": id}
    expires = datetime.utcnow() + timedelta(minutes=EXPIRES_MINUTES)
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

# get current user from token
async def get_current_user(db: Session, token: str = Depends(oaut2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        id: int = payload.get("id")
        expires: datetime = payload.get("exp")
        if datetime.fromtimestamp(expires) < datetime.utcnow():
            return None
        if email is None or id is None:
            return None
        db_user = db.query(models.User).filter(models.User.id == id).first()
        return db_user
    except JWTError:
        return None

# Authenticate
async def authenticate(db: Session, email: str, password: str):
    db_user = get_user_by_email(db, email)
    if not db_user:
        return None
    if not bcrypt_context.verify(password, db_user.hashed_password):
        return None
    return db_user

# reset password

async def generate_code(db: Session, email: str):
    code = str(randint(1000,9999))
    db_reset = db.query(models.ResetPassword).filter(models.ResetPassword.email == email).first()
    if db_reset:
        db_reset.code = code
    else:
        db_reset = models.ResetPassword(email = email, code = code)
        db.add(db_reset)

    db.commit()
    return code

async def verify_code(db: Session, email: str, code: str):
    db_reset = db.query(models.ResetPassword).filter(models.ResetPassword.email == email).first()
    if not db_reset:
        return False
    else:
        return db_reset.code == code

async def fake_email_send(email: str, code: str):
    print(f"code {code} sent to {email}")